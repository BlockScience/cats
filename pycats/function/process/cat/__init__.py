import os, subprocess, time, json
from importlib.machinery import SourceFileLoader

import numpy as np
from multimethod import isa, overload

from pycats.structure.plant.spark import Plant
from pycats.function.process.utils import get_s3_keys, s3, _connect


class Processor(Plant):
    def __init__(self,
        plantSession = None,
        DRIVER_IPFS_DIR='/home/jjodesty/Projects/Research/cats/cadStore'
    ):
        Plant.__init__(self, plantSession)
        self.DRIVER_IPFS_DIR = DRIVER_IPFS_DIR

        self.cai_invoice_cid = None
        self.cao_invoice_cid: str = None
        self.transform_func = None
        # self.transform_cid = None

        self.cai_bom_cid = None
        self.cai_bom = {}
        self.cao_bom = {}

        self.ipfs_id = None
        self.daemon_pid = None
        self.daemon_proc = None
        self.ip4_tcp_addresses = None

    def start_daemon(self):
        ipfs_daemon = f'ipfs daemon'
        self.daemon_proc = subprocess.Popen(
            ipfs_daemon, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self.daemon_pid = self.daemon_proc.pid
        time.sleep(15)
        ipfs_id_cmd = f'ipfs id > {self.DRIVER_IPFS_DIR}/ipfs_id.json'
        output = subprocess.check_output(ipfs_id_cmd, shell=True)
        self.ipfs_id = open(f'{self.DRIVER_IPFS_DIR}/ipfs_id.json') # ToDO: change from file
        ipfs_addresses = json.load(self.ipfs_id)["Addresses"]
        self.ip4_tcp_addresses = [
            x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x) and ('172.17.0.3' not in x)
        ]
        return self

    def get_driver_ipfs_id(self):
        self.ipfs_id = open(f'{self.DRIVER_IPFS_DIR}/ipfs_id.json') # ToDO: change from file
        ipfs_addresses = json.load(self.ipfs_id)["Addresses"]
        self.ip4_tcp_addresses = [
            x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x) and ('172.17.0.3' not in x)
        ]
        return self

    def content_address_dataset(self, bucket, input_path, cai_invoice_uri):
        s3_input_keys = get_s3_keys(bucket, input_path)
        input_cad_invoice = self.generate_input_invoice(s3_input_keys, cai_invoice_uri)
        invoice_cid, ip4_tcp_addresses = self.cid_input_invoice(cai_invoice_uri)
        return input_cad_invoice, str(invoice_cid), ip4_tcp_addresses

    def content_address_input(
            self,
            input_data_uri,
            invoice_uri,
            output_data_uri,
            bom_write_path_uri,
            local_bom_write_path='/tmp/bom.json',
            transformer_uri=None):
        self.catContext['cai_invoice_uri'] = invoice_uri

        self.cai_bom['transformer_uri'] = transformer_uri
        self.cai_bom['cai_invoice_uri'] = invoice_uri
        self.cai_bom['cai_data_uri'] = output_data_uri
        self.cai_bom['bom_uri'] = bom_write_path_uri
        self.cai_bom['action'] = ''
        self.cai_bom['input_bom_cid'] = ''
        self.cai_bom = self.content_address_transformer(self.cai_bom)

        bucket = input_data_uri.split('s3://')[1].split('/')[0]
        input_path = input_data_uri.split('s3://')[1].split(bucket)[1][1:]+'/'
        (
            input_cad_invoice,
            self.cai_bom['invoice_cid'],
            ip4_tcp_addresses
        ) = self.content_address_dataset(bucket, input_path, self.catContext['cai_invoice_uri'])
        self.cai_bom['addresses'] = np.unique(
            np.array(ip4_tcp_addresses)
        ).tolist()
        self.cai_bom = self.save_bom(self.cai_bom, 'cai')
        self.cai_invoice_cid = self.cai_bom['invoice_cid']
        cai_bom_df = self.create_bom_df(self.cai_bom)
        # cai_bom_df.write.json(self.cai_bom_uri, mode='overwrite')
        # return input_cad_invoice
        with open(local_bom_write_path, 'w') as fp:
            cai_bom_dict = self.bom_df_to_dict(cai_bom_df)
            json.dump(cai_bom_dict, fp)

        if 's3a://' in bom_write_path_uri:
            bom_write_path_uri = bom_write_path_uri.replace('s3a://', 's3://')

        aws_cp = f'aws s3 cp {local_bom_write_path} {bom_write_path_uri}'
        subprocess.check_call(aws_cp.split(' '))
        return cai_bom_dict, input_cad_invoice


    def content_address_output(self, cao_bom: isa(dict), local_bom_write_path: isa(str)):
        cai_data_uri = cao_bom['cai_data_uri']  # I
        cai_invoice_uri = cao_bom['cai_invoice_uri']  # O
        s3_bom_write_path = cao_bom['cad_bom_uri']  # O
        cao_bom['cao_data_uri'] = ''
        cao_bom['action'] = ''
        self.cao_bom = self.content_address_transformer(cao_bom)

        if 's3a://' in cai_data_uri:
            cai_data_uri = cai_data_uri.replace("s3a:", "s3:")
        bucket = cai_data_uri.split('s3://')[1].split('/')[0]
        input_path = cai_data_uri.split('s3://')[1].split(bucket)[1][1:] + '/'

        (
            output_cad_invoice,
            self.cao_bom['invoice_cid'],
            ip4_tcp_addresses
        ) = self.content_address_dataset(bucket, input_path, cai_invoice_uri)
        self.cao_bom['addresses'] = np.unique(
            np.array(ip4_tcp_addresses)
        ).tolist()
        self.cao_bom = self.save_bom(self.cao_bom, 'cao')
        cao_bom_df = self.create_bom_df(self.cao_bom)
        with open(local_bom_write_path, 'w') as fp:
            cao_bom_dict = self.bom_df_to_dict(cao_bom_df)
            json.dump(cao_bom_dict, fp)

        if 's3a://' in s3_bom_write_path:
            s3_bom_write_path = s3_bom_write_path.replace('s3a://', 's3://')
        aws_cp = f'aws s3 cp {local_bom_write_path} {s3_bom_write_path}'
        subprocess.check_call(aws_cp.split(' '))
        self.write_rdd_as_parquet(output_cad_invoice, self.cao_bom['cai_invoice_uri'])
        return cao_bom_dict, output_cad_invoice

    def get_bom_from_s3(self, bom_path, tmp_bom_filepath):
        bom_bucket = bom_path.split('s3://')[1].split('/')[0]
        bom_prefix = bom_path.split('s3://')[1].split(bom_bucket)[1][1:]
        s3.download_file(Bucket=bom_bucket, Key=bom_prefix, Filename=tmp_bom_filepath)
        with open(tmp_bom_filepath) as bom_file:
            bom = json.load(bom_file)
        bom_file.close()
        return bom

    def get_input_bom_from_s3(self, input_bom_path, tmp_bom_filepath='/tmp/input_bom.json'):
        return self.get_bom_from_s3(input_bom_path, tmp_bom_filepath)

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

    def set_cao_bom(self, ip4_tcp_addresses, cai_bom, output_bom_path):
        cao_bom = {}
        cao_bom['action'] = ''
        cao_bom['addresses'] = ip4_tcp_addresses
        cao_bom['input_bom_cid'] = cai_bom['bom_cid']
        cao_bom['cai_invoice_uri'] = ''
        cao_bom['invoice_cid'] = ''  # rename to cai_invoice_cid
        cao_bom['transform_cid'] = ''
        cao_bom['transform_filename'] = ''
        cao_bom['transform_node_path'] = ''
        cao_bom['transform_uri'] = ''
        cao_bom['cad_bom_uri'] = output_bom_path
        return cao_bom

    @overload
    def transform(
            self,
            cai_bom: isa(dict),
            cao_bom: isa(dict)
    ):
        self.cai_invoice_uri = cai_bom['cai_invoice_uri']
        self.cao_data_uri = cai_bom['cao_data_uri']
        catContext = self.cad.execute(
            cai_invoice_uri=self.cai_invoice_uri,
            cao_data_uri=self.cao_data_uri,
            transform_func=self.transform_func
        )
        self.write_df_as_parquet(catContext['cao'], cao_bom['cai_data_uri'])
        return catContext, cai_bom, cao_bom

    @overload
    def transform(
            self,
            input_bom_path: isa(str),
            output_bom_path: isa(str),
            input_bom_update: isa(dict) = None,
            output_bom_update: isa(dict) = None
    ):
        self.cai_bom = self.get_input_bom_from_s3(input_bom_path)
        if input_bom_update is not None:
            self.cai_bom.update(input_bom_update)

        _connect(self.cai_bom['addresses'])

        self.transform_func = self.get_transform_func(self.cai_bom)

        self.cao_bom = self.set_cao_bom(
            self.ip4_tcp_addresses, self.cai_bom, output_bom_path
        )
        if output_bom_update is not None:
            self.cao_bom.update(output_bom_update)
            self.catContext, self.cai_bom, self.cao_bom = self.transform(self.cai_bom, self.cao_bom)

            with open(self.cao_bom['transform_sourcefile'], 'rb') as cao_transform_file:
                bucket = self.cao_bom['transformer_uri'].split('s3a://')[1].split('/')[0]
                prefix = self.cao_bom['transformer_uri'].split('s3a://')[1].split(bucket)[1][1:]
                s3.upload_fileobj(cao_transform_file, Bucket=bucket, Key=prefix)
            cao_transform_file.close()

            self.cao_bom, output_cad_invoice = self.content_address_output(
                cao_bom=self.cao_bom,
                local_bom_write_path='/tmp/bom.json'
            )
        else:
            self.catContext, self.cai_bom, self.cao_bom = self.transform(self.cai_bom, self.cao_bom)

        CAO_BOM_FILE_PATH = '/tmp/output_bom.json'
        with open(CAO_BOM_FILE_PATH, 'w') as f:
            json.dump(self.cao_bom, f)
            ipfs_add = f'ipfs add {CAO_BOM_FILE_PATH}'.split(' ')
            [_, self.cao_bom['cad_cid'], _] = subprocess.check_output(ipfs_add) \
                .decode('ascii').replace('\n', '').split(' ')
            json.dump(self.cao_bom, f)
        f.close()
        with open(CAO_BOM_FILE_PATH, 'rb') as f:
            output_bom_bucket = self.cao_bom['cad_bom_uri'].split('s3://')[1].split('/')[0]
            output_bom_prefix = self.cao_bom['cad_bom_uri'].split('s3://')[1].split(output_bom_bucket)[1][1:]
            s3.upload_fileobj(f, Bucket=output_bom_bucket, Key=output_bom_prefix)
        f.close()
        return self