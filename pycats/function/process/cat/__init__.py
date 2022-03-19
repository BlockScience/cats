import json
import numpy as np
from multimethod import isa, overload
from pycats.structure.plant.spark import Plant


class Processor(Plant):
    def __init__(self,
        plantSession,
        DRIVER_IPFS_DIR='/home/jjodesty/Projects/Research/cats/cadStore'
    ):
        Plant.__init__(self, plantSession, DRIVER_IPFS_DIR)

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

    @overload
    def content_address_dataset(self, s3_bucket, s3_prefix, cai_invoice_uri):
        s3_input_keys = self.get_s3_keys(s3_bucket, s3_prefix)
        return self.create_invoice(s3_input_keys, cai_invoice_uri)

    @overload
    def content_address_dataset(self, s3_dataset_uri, cai_invoice_uri):
        dataset_s3_bucket, dataset_s3_prefix = self.get_s3_bucket_prefix_pair(s3_dataset_uri)
        return self.content_address_dataset(dataset_s3_bucket, dataset_s3_prefix, cai_invoice_uri)

    def content_address_input(
            self,
            input_data_uri,
            invoice_uri,
            output_data_uri,
            bom_write_path_uri,
            local_bom_write_path='/tmp/bom.json',
            transformer_uri=None
    ):
        self.catContext['cai_invoice_uri'] = invoice_uri

        self.cai_bom['transformer_uri'] = transformer_uri
        self.cai_bom['cai_invoice_uri'] = invoice_uri
        self.cai_bom['cai_data_uri'] = output_data_uri
        self.cai_bom['bom_uri'] = bom_write_path_uri
        self.cai_bom['action'] = ''
        self.cai_bom['input_bom_cid'] = ''
        self.cai_bom = self.content_address_transform(self.cai_bom) # ToDo: make generic for plant

        (
            input_cad_invoice,
            self.cai_bom['invoice_cid'],
            ip4_tcp_addresses
        ) = self.content_address_dataset(input_data_uri, self.catContext['cai_invoice_uri'])
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

        # self.boto3_cp(local_bom_write_path, bom_write_path_uri)
        self.aws_cli_cp(local_bom_write_path, bom_write_path_uri)
        return cai_bom_dict, input_cad_invoice

    def content_address_output(self, cao_bom: isa(dict), local_bom_write_path: isa(str)):
        cai_data_uri = cao_bom['cai_data_uri']  # I
        cai_invoice_uri = cao_bom['cai_invoice_uri']  # O
        s3_bom_write_path = cao_bom['cad_bom_uri']  # O
        cao_bom['cao_data_uri'] = ''
        cao_bom['action'] = ''
        self.cao_bom = self.content_address_transform(cao_bom) # ToDo: make generic for plant

        if 's3a://' in cai_data_uri:
            cai_data_uri = cai_data_uri.replace("s3a:", "s3:")
        (
            output_cad_invoice,
            self.cao_bom['invoice_cid'],
            ip4_tcp_addresses
        ) = self.content_address_dataset(cai_data_uri, cai_invoice_uri)
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
        # upload
        self.aws_cli_cp(local_bom_write_path, s3_bom_write_path)
        self.write_rdd_as_parquet(output_cad_invoice, self.cao_bom['cai_invoice_uri'])
        return cao_bom_dict, output_cad_invoice

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

        self.ipfs_swarm_connect(self.cai_bom['addresses'])

        self.transform_func = self.get_transform_func(self.cai_bom)

        self.cao_bom = self.set_cao_bom(self.ip4_tcp_addresses, self.cai_bom, output_bom_path)
        if output_bom_update is not None:
            self.cao_bom.update(output_bom_update)
            self.catContext, self.cai_bom, self.cao_bom = self.transform(self.cai_bom, self.cao_bom)

            with open(self.cao_bom['transform_sourcefile'], 'rb') as cao_transform_file:
                transformer_bucket, transformer_key = self.get_s3_bucket_key_pair(self.cao_bom['transformer_uri'])
                self.s3_client.upload_fileobj(cao_transform_file, Bucket=transformer_bucket, Key=transformer_key)
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
            [_, self.cao_bom['cad_cid'], _] = self.ipfs_add(CAO_BOM_FILE_PATH)
            json.dump(self.cao_bom, f)
        f.close()
        with open(CAO_BOM_FILE_PATH, 'rb') as f:
            output_bom_bucket, output_bom_key = self.get_s3_bucket_key_pair(self.cao_bom['cad_bom_uri'])
            self.s3_client.upload_fileobj(f, Bucket=output_bom_bucket, Key=output_bom_key)
        f.close()

        return self