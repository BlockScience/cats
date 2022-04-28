import os, subprocess, json
from copy import deepcopy
from importlib.machinery import SourceFileLoader

from pycats import CATS_HOME
from pycats.function import TRANSFORM_DIR, IPFS_DIR, INPUT_DIR
from pycats.function.infrafunction.client.s3 import Client as S3client
from pycats.function.infrafunction.client.ipfs import IPFS as IPFSclient


class ProcessClient(S3client, IPFSclient):
    def __init__(self,
        DRIVER_IPFS_DIR=f'{CATS_HOME}/cadStore'
    ):
        self.DRIVER_IPFS_DIR = DRIVER_IPFS_DIR
        S3client.__init__(self)
        IPFSclient.__init__(self, DRIVER_IPFS_DIR)

    def get_driver_ipfs_id(self):
        self.ipfs_id = open(f'{self.DRIVER_IPFS_DIR}/ipfs_id.json') # ToDO: change from file
        ipfs_addresses = json.load(self.ipfs_id)["Addresses"]
        self.ip4_tcp_addresses = [
            x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x) and ('172.17.0.3' not in x)
        ]
        return self

    def get_transform_func(self, bom):
        # transform_filename = bom['transform_sourcefile'].split('/')[-1]
        transform_filename = bom['transform_filename']
        os.chdir('/tmp/')
        subprocess.check_call(f"ipfs get {bom['transform_cid']}", shell=True)
        subprocess.check_call(f"mv {bom['transform_cid']} {transform_filename}", shell=True)
        tmp_transform_sourcefile = f"/tmp/{transform_filename}"
        transform = SourceFileLoader(
            "transform",
            tmp_transform_sourcefile
        ).load_module()
        return transform.transform

    def get_transform_func_s3(self, bom):
        transform_uri = deepcopy(bom['transform_uri'])
        if 's3a://' in transform_uri:
            transform_uri = transform_uri.replace('s3a://', 's3://')

        os.chdir('/tmp/')
        self.aws_cli_cp(transform_uri, f"./{bom['transform_filename']}")
        tmp_transform_sourcefile = f"/tmp/{bom['transform_filename']}"
        transform = SourceFileLoader(
            "transform",
            tmp_transform_sourcefile
        ).load_module()
        return transform.transform

    def get_input_bom_from_s3(self, input_bom_path, tmp_bom_filepath='/tmp/input_bom.json'):
        return self.download_dict_file(input_bom_path, tmp_bom_filepath)

    def get_input_log_from_s3(self, input_bom_path, tmp_bom_filepath='/tmp/input_bom.json'):
        return self.download_dict_file(input_bom_path, tmp_bom_filepath)

    def content_address_transformer(self, transform_uri):
        # 's3a://cats-public/cad-store/cad/transformation/transform.py'
        transform_bucket = transform_uri.split('s3a://')[-1].split('/')[0]
        transform_key = transform_uri.split('s3a://')[-1].split(transform_bucket)[-1][1:]
        transform_filename = transform_key.split('/')[-1]
        NODE_FILE_PATH = f"{TRANSFORM_DIR}/{transform_filename}"

        subprocess.check_call(f"mkdir -p {TRANSFORM_DIR}".split(' '))
        # if doesnt exist
        self.s3_client.download_file(Bucket=transform_bucket, Key=transform_key, Filename=NODE_FILE_PATH)
        ipfs_add = f'ipfs add {NODE_FILE_PATH}'.split(' ')
        [ipfs_action, cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')

        ipfs_id = open(f'{IPFS_DIR}/ipfs_id.json')
        ipfs_addresses = json.load(ipfs_id)["Addresses"]
        ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]

        partial_bom = {
            'action': ipfs_action,
            'transform_cid': cid,
            'transform_uri': transform_uri,
            'transformer_addresses': ip4_tcp_addresses,
            'transform_filename': transform_filename,
            'transform_node_path': NODE_FILE_PATH
        }
        return partial_bom

    def get_bom(self, x):
        bom_cid, addresses = x[0], x[1]
        subprocess.check_call(f"mkdir -p {INPUT_DIR}".split(' '))
        os.chdir(INPUT_DIR)

        self.ipfs_swarm_connect(addresses)
        output = subprocess.check_output(f"ipfs get {bom_cid}".split(' ')).decode('ascii').replace('\n', '')
        subprocess.check_call(f"mv {bom_cid} bom.json".split(' '))
        bom_file = open(f'{INPUT_DIR}/bom.json')
        bom = json.load(bom_file)  # ["addresses"]
        return bom