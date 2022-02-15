import os, subprocess, time, json, boto3
from copy import deepcopy
from importlib.machinery import SourceFileLoader

import numpy as np
from multimethod import isa, overload
from pyspark import RDD
from pyspark.sql import SparkSession, DataFrame

from pycats.function.process.utils import \
    cluster_fs_ingest, get_upload_path, get_s3_keys, cad_invoicing, s3, ipfs_caching, \
    content_address_transformer, save_bom, save_invoice, get_bom, transfer_invoice, _connect, ipfs_connect, link_ipfs_id

s3 = boto3.client(
    's3',
    region_name='us-east-2',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)

class CAD(object): # CAD invoice of partition transactions
    def __init__(self,
        spark: SparkSession,
        df: DataFrame = None,
        cai_ingest_func = lambda part_invoice: cluster_fs_ingest(json.loads(part_invoice))
    ):
        self.spark: SparkSession = spark
        self.sc = spark.sparkContext
        self.cai_ingest_func = cai_ingest_func
        self.transform_func = None
        self.catContext: dict = None

        # self.invoiceURI = None
        # self.invoice = None
        # self.transformer_uri = None
        # self.bom = self.content_address_transform(self.transformer_uri)
        self.df = df

    @overload
    def read(self, invoice: isa(RDD)):
        data_uri = invoice.map(get_upload_path).distinct().collect()[0]
        # get cai_invoice_uri
        df: DataFrame = self.spark.read.parquet(data_uri)
        self.catContext = {
            'cai': df,
            'cai_invoice': invoice,
            'cai_data_uri': data_uri,
        }
        return self.catContext

    @overload
    def read(self, invoice_uri: isa(str)):
        invoice_rdd = self.sc.textFile(invoice_uri).map(self.cai_ingest_func)
        # self.catContext['cai_invoice_uri'] = invoice_uri
        return self.read(invoice_rdd)

    @overload
    def transform(self, transform_func, invoice_uri: isa(str) = None):
        self.transform_func = transform_func
        if self.catContext['cai'] is not None or invoice_uri is None:
            self.df = self.transform_func(self)
            self.catContext['cao'] = self.df
            return self.catContext
        elif self.catContext['cai'] is None or invoice_uri is not None:
            self.catContext = self.read(invoice_uri)
            self.df = self.transform_func(self)
            self.catContext['cao'] = self.df
            return self.catContext

    @overload
    def transform(self, transform_func, invoice: isa(RDD) = None):
        self.transform_func = transform_func
        if self.catContext['cai'] is not None or invoice is None:
            self.df = self.transform_func(self)
            self.catContext['cao'] = self.df
            return self.catContext
        elif self.catContext['cai'] is None or invoice is not None:
            self.catContext = self.read(invoice)
            self.df = self.transform_func(self)
            self.catContext['cao'] = self.df
            return self.catContext

    def write(self, cad_data_uri: str):
        self.df.write.parquet(cad_data_uri, mode='overwrite')
        self.catContext['cao_data_uri'] = cad_data_uri

    @overload
    def execute(self, cai_invoice_uri: isa(str), cao_data_uri: isa(str), transform_func):
        self.catContext = self.read(cai_invoice_uri)
        self.transform(transform_func, cai_invoice_uri)
        self.write(cao_data_uri)
        self.catContext['cao_data_uri'] = cao_data_uri
        self.catContext['cai_invoice_uri'] = cai_invoice_uri
        self.catContext['cao_invoice_uri'] = f"{cao_data_uri.split('/parts')[0]}/invoices"
        return self.catContext

    @overload
    def execute(self, cai_invoice: isa(RDD), cao_data_uri: isa(str), transform_func):
        self.catContext = self.read(cai_invoice)
        self.transform(transform_func, cai_invoice)
        self.write(cao_data_uri)
        self.catContext['cao_data_uri'] = cao_data_uri
        # self.catContext['cai_invoice_uri'] = cai_invoice_uri
        self.catContext['cao_invoice_uri'] = f"{cao_data_uri.split('/parts')[0]}/invoices"
        return self.catContext


class Processor(object):
    def __init__(self,
        sparkSession: SparkSession,
        DRIVER_IPFS_DIR='/home/jjodesty/Projects/Research/cats/cadStore'
    ):
        self.spark: SparkSession = sparkSession
        self.sc = self.spark.sparkContext
        self.sc._jsc. \
            hadoopConfiguration().set("mapreduce.input.fileinputformat.input.dir.recursive", "true")
        self.DRIVER_IPFS_DIR = DRIVER_IPFS_DIR
        self.cad: CAD = CAD(
            spark=self.spark
        )

        self.cai_invoice_cid = None
        self.cao_invoice_cid: str = None
        self.transform_func = None
        # self.transform_cid = None

        self.catContext = {}
        self.cai_bom_cid = None
        self.cai: DataFrame = None
        self.cao: DataFrame = None
        self.caiInvoice: RDD = None
        self.caoInvoice: RDD = None
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


    def content_address_transformer(self, bom):
        if bom['transformer_uri'] is not None:
            self.transformer_uri = bom['transformer_uri']
            partial_bom: dict = self.spark.sparkContext \
                .parallelize([self.transformer_uri]) \
                .repartition(1) \
                .map(content_address_transformer) \
                .collect()[0]
            bom.update(partial_bom)
        else:
            bom['transform_cid'] = ''
            bom['transform_uri'] = ''
            bom['transformer_addresses'] = ''
            bom['transform_filename'] = ''
            bom['transform_node_path'] = ''
            raise Exception('transformer_uri is None')
        return bom


    def content_address_dataset(self, bucket, input_path, cai_invoice_uri):
        s3_input_keys = get_s3_keys(bucket, input_path)
        partition_count = len(s3_input_keys)
        input_cad_invoice: RDD = self.sc \
            .parallelize(s3_input_keys) \
            .repartition(partition_count) \
            .map(ipfs_caching) # .map(lambda x: link_ipfs_id(x))
        input_cad_invoice_df: DataFrame = input_cad_invoice.toDF()
        input_cad_invoice_df.write.json(cai_invoice_uri, mode='overwrite')
        invoice_cid, ip4_tcp_addresses = self.sc \
            .parallelize([cai_invoice_uri]) \
            .repartition(1) \
            .map(save_invoice) \
            .collect()[0]
        return input_cad_invoice, str(invoice_cid), ip4_tcp_addresses


    def content_address_input(
            self,
            s3_input_data_path,
            cai_invoice_uri,
            cao_data_uri,
            s3_bom_write_path,
            local_bom_write_path='/tmp/bom.json',
            transformer_uri=None):
        self.catContext['cai_invoice_uri'] = cai_invoice_uri

        self.cai_bom['transformer_uri'] = transformer_uri
        self.cai_bom['cai_invoice_uri'] = cai_invoice_uri
        self.cai_bom['cao_data_uri'] = cao_data_uri
        self.cai_bom['cad_bom_uri'] = s3_bom_write_path
        self.cai_bom['action'] = ''
        self.cai_bom['cai_cid'] = ''
        self.cai_bom = self.content_address_transformer(self.cai_bom)
        # self.cai_bom = self.content_address_transformer(self.cai_bom)

        bucket = s3_input_data_path.split('s3://')[1].split('/')[0]
        input_path = s3_input_data_path.split('s3://')[1].split(bucket)[1][1:]+'/'
        (
            input_cad_invoice,
            self.cai_bom['invoice_cid'],
            ip4_tcp_addresses
        ) = self.content_address_dataset(bucket, input_path, self.catContext['cai_invoice_uri'])
        self.cai_bom['addresses'] = np.unique(
            np.array(ip4_tcp_addresses)
        ).tolist()
        cai_bom_rdd = self.sc \
            .parallelize([self.cai_bom]) \
            .repartition(1) \
            .map(save_bom('cai'))
        self.cai_bom = cai_bom_rdd.collect()[0]
        self.cai_invoice_cid = self.cai_bom['invoice_cid']
        cai_bom_df = self.spark.createDataFrame([self.cai_bom]).repartition(1)
        # cai_bom_df.write.json(self.cai_bom_uri, mode='overwrite')
        # return input_cad_invoice
        with open(local_bom_write_path, 'w') as fp:
            cai_bom_dict = cai_bom_df.rdd.map(lambda row: row.asDict()).collect()[0]
            json.dump(cai_bom_dict, fp)

        if 's3a://' in s3_bom_write_path:
            s3_bom_write_path = s3_bom_write_path.replace('s3a://', 's3://')

        aws_cp = f'aws s3 cp {local_bom_write_path} {s3_bom_write_path}'
        subprocess.check_call(aws_cp.split(' '))
        return cai_bom_dict, input_cad_invoice


    def content_address_output(self, cao_bom: isa(dict), local_bom_write_path: isa(str)):
        s3_input_data_path = cao_bom['cai_data_uri']  # I
        cai_invoice_uri = cao_bom['cai_invoice_uri']  # O
        s3_bom_write_path = cao_bom['cad_bom_uri']  # O
        cao_bom['cao_data_uri'] = ''
        cao_bom['action'] = ''
        cao_bom = self.content_address_transformer(cao_bom)

        if 's3a://' in s3_input_data_path:
            s3_input_data_path = s3_input_data_path.replace("s3a:", "s3:")
        bucket = s3_input_data_path.split('s3://')[1].split('/')[0]
        input_path = s3_input_data_path.split('s3://')[1].split(bucket)[1][1:] + '/'

        (
            output_cad_invoice,
            cao_bom['invoice_cid'],
            ip4_tcp_addresses
        ) = self.content_address_dataset(bucket, input_path, cai_invoice_uri)
        cao_bom['addresses'] = np.unique(
            np.array(ip4_tcp_addresses)
        ).tolist()
        cao_bom_rdd = self.sc \
            .parallelize([cao_bom]) \
            .repartition(1) \
            .map(save_bom('cao'))
        cao_bom = cao_bom_rdd.collect()[0]
        cao_bom_df = self.spark.createDataFrame([cao_bom]).repartition(1)

        with open(local_bom_write_path, 'w') as fp:
            cao_bom_dict = cao_bom_df.rdd.map(lambda row: row.asDict()).collect()[0]
            json.dump(cao_bom_dict, fp)

        if 's3a://' in s3_bom_write_path:
            s3_bom_write_path = s3_bom_write_path.replace('s3a://', 's3://')
        aws_cp = f'aws s3 cp {local_bom_write_path} {s3_bom_write_path}'
        subprocess.check_call(aws_cp.split(' '))

        return cao_bom_dict, output_cad_invoice

    def get_bom_worker(self, addresses, bom_cid):
        bom_rdd: RDD = self.spark.sparkContext \
            .parallelize([
                [
                    bom_cid,
                    addresses
                ]
            ]) \
            .repartition(1) \
            .map(get_bom).map(transfer_invoice)

        bom = bom_rdd.collect()[0]
        return bom


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
        cao_bom['cai_cid'] = cai_bom['cad_cid']
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
        catContext['cao'].write.parquet(cao_bom['cai_data_uri'], mode='overwrite')
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
            output_cad_invoice.toDF().write.parquet(self.cao_bom['cai_invoice_uri'], mode='overwrite')
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