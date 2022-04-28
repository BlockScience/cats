import json
import os
import subprocess

from pycats import CATS_HOME
from pycats.function.process.cat import Processor
from pycats.utils import subproc_stout, build_software
from pycats.function.infrafunction.plant.spark import spark_submit
from pycats.function.infrafunction.client.s3 import Client as S3client


class Executor:
    def __init__(self,
        terraform_cmd: str = None,
        SPARK_HOME: str = None,
        CAT_APP_HOME: str = None,
        TRANSFORM_SOURCE: str = None,
        TRANSFORM_DEST: str = None
    ):
        self.terraform_cmd = terraform_cmd
        self.SPARK_HOME = SPARK_HOME
        self.CAT_APP_HOME = CAT_APP_HOME
        self.TRANSFORM_SOURCE = TRANSFORM_SOURCE
        self.TRANSFORM_DEST = TRANSFORM_DEST

    def build_cats(self):
        build_software()
        return self

    def terraform(self, terraform_cmd=None):
        if terraform_cmd is not None:
            self.terraform_cmd = terraform_cmd
        subproc_stout(self.terraform_cmd)
        return self

    def execute(self,
        SPARK_HOME=None,
        CAT_APP_HOME=None,
        TRANSFORM_SOURCE=None,
        TRANSFORM_DEST=None
    ):
        if SPARK_HOME is not None \
                or CAT_APP_HOME is not None \
                or TRANSFORM_SOURCE is not None \
                or TRANSFORM_DEST is not None:
            self.SPARK_HOME = SPARK_HOME,
            self.CAT_APP_HOME = CAT_APP_HOME,
            self.TRANSFORM_SOURCE = TRANSFORM_SOURCE,
            self.TRANSFORM_DEST = TRANSFORM_DEST

        spark_submit(
            self.SPARK_HOME,
            self.CAT_APP_HOME,
            self.TRANSFORM_SOURCE,
            self.TRANSFORM_DEST
        )
        return self


# ToDO: add local transformer path as configuration
# ToDO: move & rename input_bom_path to bom_uri
# ToDo: bom creation and mutation occur on driver
class Factory(Executor, S3client):
    def __init__(self,
        plantSession,
        terraform_cmd: str,
        terraform_file: str,
        DRIVER_IPFS_DIR: str = f'{CATS_HOME}/cadStore',
        SPARK_HOME: str = None,
        CAT_APP_HOME: str = None,
        TRANSFORM_SOURCE: str = None,
        TRANSFORM_DEST: str = None,

    ):
        self.SPARK_HOME = SPARK_HOME
        self.CAT_APP_HOME = CAT_APP_HOME
        self.TRANSFORM_SOURCE = TRANSFORM_SOURCE
        self.TRANSFORM_DEST = TRANSFORM_DEST

        Executor.__init__(
            self,
            self.SPARK_HOME,
            self.CAT_APP_HOME,
            self.TRANSFORM_SOURCE,
            self.TRANSFORM_DEST
        )
        S3client.__init__(self)
        self.processor: Processor = None
        self.partial_log = {}
        self.partial_bom = {}
        self.partial_bom['terraform_file'] = terraform_file

        self.plantSession = plantSession
        self.DRIVER_IPFS_DIR = DRIVER_IPFS_DIR
        self.terraform_cmd = terraform_cmd
        self.SPARK_HOME = SPARK_HOME
        self.CAT_APP_HOME = CAT_APP_HOME
        self.TRANSFORM_SOURCE = TRANSFORM_SOURCE
        self.TRANSFORM_DEST = TRANSFORM_DEST

    def init_processor(self):
        self.partial_bom, self.partial_log = self.content_address_terraform()
        self.processor = Processor(
            self.plantSession(), self.DRIVER_IPFS_DIR, self.partial_bom, self.partial_log
        )
        return self.processor

    def content_address_terraform(self):
        if self.partial_bom['terraform_file'] is not None:
            TMP_DIR = '/tmp'
            self.terraform_file = self.partial_bom['terraform_file']
            tf_filename = self.terraform_file.split('/')[-1]
            NODE_FILE_PATH = f"{TMP_DIR}/{tf_filename}"

            ipfs_add = f'ipfs add {self.terraform_file}'.split(' ')
            [ipfs_action, cid, _file_name] = subprocess \
                .check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')

            with open(f'{TMP_DIR}/ipfs_id.json', 'w') as fp:
                pass
            fp.close()
            os.chdir(TMP_DIR)
            subprocess.check_output(f'ipfs id > ipfs_id.json', shell=True)
            ipfs_id_file = open(f'ipfs_id.json')
            ipfs_addresses = json.load(ipfs_id_file)["Addresses"]
            ipfs_id_file.close()
            ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]

            self.partial_log['terraform_addresses'] = ip4_tcp_addresses
            self.partial_bom['terraform_cid'] = cid
            self.partial_bom['terraform_filename'] = tf_filename
            self.partial_bom['terraform_node_path'] = NODE_FILE_PATH
        else:
            self.partial_log['terraform_addresses'] = ''
            self.partial_bom['terraform_cid'] = ''
            self.partial_bom['terraform_filename'] = ''
            self.partial_bom['terraform_node_path'] = ''
        return self.partial_bom, self.partial_log








