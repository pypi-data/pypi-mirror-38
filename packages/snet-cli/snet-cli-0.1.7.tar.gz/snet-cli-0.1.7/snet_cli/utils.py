import _md5
import json
import os
from pathlib import Path

import web3
import pkg_resources
from grpc_tools.protoc import main as protoc

from snet_cli.identity import RpcIdentityProvider, MnemonicIdentityProvider, TrezorIdentityProvider, \
    LedgerIdentityProvider, KeyIdentityProvider


class DefaultAttributeObject(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)

    def getstring(self, item):
        return getattr(self, item)

    def getint(self, item):
        if getattr(self, item) is None:
            return None
        return int(getattr(self, item))

    def getfloat(self, item):
        if getattr(self, item) is None:
            return None
        return float(getattr(self, item))

    def getboolean(self, item):
        if getattr(self, item) is None:
            return None
        i = self.getstring(item)
        if i in ["yes", "on", "true", "True", "1"]:
            return True
        return False

    def __getattr__(self, item):
        return self.__dict__.get(item, None)

    def __repr__(self):
        return self.__dict__.__repr__()

    def __str__(self):
        return self.__dict__.__str__()


def get_identity(w3, session, args):
    if session.identity is None:
        pass
    if session.identity.identity_type == "rpc":
        return RpcIdentityProvider(w3, getattr(args, "wallet_index", None) or session.getint("default_wallet_index"))
    if session.identity.identity_type == "mnemonic":
        return MnemonicIdentityProvider(w3, session.identity.mnemonic,
                                        getattr(args, "wallet_index", None) or session.getint("default_wallet_index"))
    if session.identity.identity_type == "trezor":
        return TrezorIdentityProvider(w3, getattr(args, "wallet_index", None) or session.getint("default_wallet_index"))
    if session.identity.identity_type == "ledger":
        return LedgerIdentityProvider(w3, getattr(args, "wallet_index", None) or session.getint("default_wallet_index"))
    if session.identity.identity_type == "key":
        return KeyIdentityProvider(w3, session.identity.private_key)


def get_web3(rpc_endpoint):
    if rpc_endpoint.startswith("ws:"):
        provider = web3.WebsocketProvider(rpc_endpoint)
    else:
        provider = web3.HTTPProvider(rpc_endpoint)

    return web3.Web3(provider)


def serializable(o):
    if isinstance(o, bytes):
        return o.hex()
    else:
        return o.__dict__


def type_converter(t):
    if t.endswith("[]"):
        return lambda x: list(map(type_converter(t.replace("[]", "")), json.loads(x)))
    else:
        if "int" in t:
            return lambda x: web3.Web3.toInt(text=x)
        elif "bytes32" in t:
            return lambda x: web3.Web3.toBytes(text=x).ljust(32, b"\0") if not x.startswith("0x") else web3.Web3.toBytes(hexstr=x).ljust(32, b"\0")
        elif "byte" in t:
            return lambda x: web3.Web3.toBytes(text=x) if not x.startswith("0x") else web3.Web3.toBytes(hexstr=x)
        elif "address" in t:
            return web3.Web3.toChecksumAddress
        else:
            return str


def _add_next_paths(path, entry_path, seen_paths, next_paths):
    with open(path) as f:
        for line in f:
            if line.strip().startswith("import"):
                import_statement = "".join(line.split('"')[1::2])
                if not import_statement.startswith("google/protobuf"):
                    import_statement_path = Path(path.parent.joinpath(import_statement)).resolve()
                    if entry_path.parent in path.parents:
                        if import_statement_path not in seen_paths:
                            seen_paths.add(import_statement_path)
                            next_paths.append(import_statement_path)
                    else:
                        raise ValueError("Path must not be a parent of entry path")


def walk_imports(entry_path):
    seen_paths = set()
    next_paths = []
    for file_path in os.listdir(entry_path):
        if file_path.endswith(".proto"):
            file_path = entry_path.joinpath(file_path)
            seen_paths.add(file_path)
            next_paths.append(file_path)
    while next_paths:
        path = next_paths.pop()
        if os.path.isfile(path):
            _add_next_paths(path, entry_path, seen_paths, next_paths)
        else:
            raise IOError("Import path must be a valid file: {}".format(path))
    return seen_paths


def get_contract_def(contract_name, contract_artifacts_root=Path(__file__).absolute().parent.joinpath("resources", "contracts")):
    contract_def = {}
    with open(Path(__file__).absolute().parent.joinpath(contract_artifacts_root, "abi", "{}.json".format(contract_name))) as f:
        contract_def["abi"] = json.load(f)
    if os.path.isfile(Path(__file__).absolute().parent.joinpath(contract_artifacts_root, "networks", "{}.json".format(contract_name))):
        with open(Path(__file__).absolute().parent.joinpath(contract_artifacts_root, "networks", "{}.json".format(contract_name))) as f:
            contract_def["networks"] = json.load(f)
    return contract_def


def read_temp_tar(f):
    f.flush()
    f.seek(0)
    return f


def get_cli_version():
    return pkg_resources.get_distribution("snet-cli").version


def compile_proto(entry_path, codegen_dir, proto_file=None):
    try:
        if not os.path.exists(codegen_dir):
            os.makedirs(codegen_dir)
        proto_include = pkg_resources.resource_filename('grpc_tools', '_proto')
        protoc_args = [
            "protoc",
            "-I{}".format(entry_path),
            '-I{}'.format(proto_include),
            "--python_out={}".format(codegen_dir),
            "--grpc_python_out={}".format(codegen_dir)
        ]
        if proto_file:
            protoc_args.append(str(proto_file))
        else:
            protoc_args.extend([str(p) for p in entry_path.glob("**/*.proto")])

        if not protoc(protoc_args):
            return True
        else:
            return False

    except Exception as e:
        return False

# return element of abi (return None if fails to find)
def abi_get_element_by_name(abi, name):
    if (abi and "abi" in abi):
        for a in abi["abi"]:
            if ("name" in a and a["name"] == name):
                return a
    return None

def abi_decode_struct_to_dict(abi, struct_list):
    return {el_abi["name"] : el for el_abi, el in zip(abi["outputs"], struct_list)}


# TODO: move get_contract_address_from_args_or_networks to the new session/config logic (issue #110)
# if arg is not None we take address from it otherwise we read the address from "networks/*json"
def get_contract_address_from_args_or_networks(w3, contract_name, arg):
    if (arg):
        return w3.toChecksumAddress(arg)
    
    # try to take address from networks
    try :
        contract_def     = get_contract_def(contract_name)
        networks         = contract_def["networks"]
        chain_id         = w3.version.network
        contract_address = networks.get(chain_id, {}).get("address", None)
        if (not contract_address):
            raise Exception()
        contract_address = w3.toChecksumAddress(contract_address)
    except:
        raise Exception("Fail to read %s address from \"networks\", you should specify address by yourself via --%s parameter"%(contract_name, contract_name.lower()))
        
    return contract_address

def get_registry_address_from_args_or_networks(w3, arg):
    return get_contract_address_from_args_or_networks(w3, "Registry", arg)

def get_mpe_address_from_args_or_networks(w3, arg):
    return get_contract_address_from_args_or_networks(w3, "MultiPartyEscrow", arg)

def get_snt_address_from_args_or_networks(w3, arg):
    return get_contract_address_from_args_or_networks(w3, "SingularityNetToken", arg)

