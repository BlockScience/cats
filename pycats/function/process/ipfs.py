import os, subprocess, json
from importlib.machinery import SourceFileLoader
# from pycats.function import TRANSFORM_DIR, IPFS_DIR
from pycats.function.infrafunction.client.s3 import Client as S3client


class Proc(S3client):
    def __init__(self,
        DRIVER_IPFS_DIR='/home/jjodesty/Projects/Research/cats/cadStore'
    ):
        self.DRIVER_IPFS_DIR = DRIVER_IPFS_DIR

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

    def get_input_bom_from_s3(self, input_bom_path, tmp_bom_filepath='/tmp/input_bom.json'):
        return self.download_dict_file(input_bom_path, tmp_bom_filepath)

    # def content_address_transformer(self, transform_uri):
    #     # 's3a://cats-public/cad-store/cad/transformation/transform.py'
    #     transform_bucket = transform_uri.split('s3a://')[-1].split('/')[0]
    #     transform_key = transform_uri.split('s3a://')[-1].split(transform_bucket)[-1][1:]
    #     transform_filename = transform_key.split('/')[-1]
    #     NODE_FILE_PATH = f"{TRANSFORM_DIR}/{transform_filename}"
    #
    #     subprocess.check_call(f"mkdir -p {TRANSFORM_DIR}".split(' '))
    #     # if doesnt exist
    #     self.s3_client.download_file(Bucket=transform_bucket, Key=transform_key, Filename=NODE_FILE_PATH)
    #     ipfs_add = f'ipfs add {NODE_FILE_PATH}'.split(' ')
    #     [ipfs_action, cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')
    #
    #     ipfs_id = open(f'{IPFS_DIR}/ipfs_id.json')
    #     ipfs_addresses = json.load(ipfs_id)["Addresses"]
    #     ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]
    #
    #     partial_bom = {
    #         'action': ipfs_action,
    #         'transform_cid': cid,
    #         'transform_uri': transform_uri,
    #         'transformer_addresses': ip4_tcp_addresses,
    #         'transform_filename': transform_filename,
    #         'transform_node_path': NODE_FILE_PATH
    #     }
    #     return partial_bom