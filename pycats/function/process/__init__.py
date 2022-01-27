import os, subprocess, time, json, boto3
from importlib.machinery import SourceFileLoader

import numpy as np
from multimethod import isa, overload
from pyspark import RDD
from pyspark.sql import SparkSession, DataFrame

from pycats.function.process.utils import \
    cluster_fs_ingest, get_upload_path, get_s3_keys, cad_invoicing, s3, ipfs_caching, \
    content_address_tranformer, save_bom, save_invoice, get_bom, transfer_invoice, _connect, ipfs_connect, link_ipfs_id


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
        self.transformer_uri = 's3a://cats-public/cad-store/cad/transformation/transform.py'
        self.bom = self.content_address_transform(self.transformer_uri)
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
        invoice = self.sc.textFile(invoice_uri).map(self.cai_ingest_func)
        self.catContext['cai_invoice_uri'] = invoice_uri
        return self.read(invoice)

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

    def content_address_transform(self, transformer_uri=None):
        if transformer_uri is not None:
            self.transformer_uri = transformer_uri
        bom: RDD = self.spark.sparkContext \
            .parallelize([self.transformer_uri]) \
            .repartition(1) \
            .map(content_address_tranformer) \
            .collect()[0]
        return bom

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
        self.ip4_tcp_addresses = self.start_daemon()

    def start_daemon(self):
        ipfs_daemon = f'ipfs daemon'
        self.daemon_proc = subprocess.Popen(
            ipfs_daemon, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self.daemon_pid = self.daemon_proc.pid
        time.sleep(15)
        ipfs_id_cmd = f'ipfs id > {self.DRIVER_IPFS_DIR}/ipfs_id.json'
        output = subprocess.check_output(ipfs_id_cmd, shell=True)
        self.ipfs_id = open(f'{self.DRIVER_IPFS_DIR}/ipfs_id.json')
        ipfs_addresses = json.load(self.ipfs_id)["Addresses"]
        ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]
        return ip4_tcp_addresses

    def init_cad(self, cai_uri, cao_uri):
        self.cai_uri: str = cai_uri
        self.cai_invoice_uri: str = f'{self.cai_uri}/invoices'  # transactions
        self.cai_data_uri: str = None  # Extend from CAD
        self.cai_bom_uri = f'{self.cai_uri}/bom'

        self.cao_uri: str = cao_uri
        self.cao_invoice_uri: str = f'{self.cao_uri}/invoices'
        self.cao_data_uri: str = f'{self.cao_uri}/parts'  # remove from CAD
        self.cao_bom_uri = f'{self.cao_uri}/bom'
        self.cao_bucket = self.cao_data_uri.split('s3a://')[-1].split('/')[0]
        self.cao_data_dir = self.cao_data_uri.split('cats-public/')[-1]

        self.cao_transform_uri: str = f'{self.cao_uri}/transformation'
        self.cao_transform_dir = self.cao_transform_uri.split('cats-public/')[-1]


        self.cai_ingest_func = lambda part_invoice: cluster_fs_ingest(json.loads(part_invoice))
        self.cad: CAD = CAD(
            spark=self.spark
        )
        self.cad.read(
            invoice=self.sc.textFile(self.cai_invoice_uri).map(self.cai_ingest_func)
        )
        self.cai_bom = {}
        self.cao_bom = self.cad.bom

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

    @overload
    def content_address_transformer(self, transformer_uri=None):
        if transformer_uri is not None:
            self.transformer_uri = transformer_uri
        bom: RDD = self.spark.sparkContext \
            .parallelize([self.transformer_uri]) \
            .repartition(1) \
            .map(content_address_tranformer) \
            .collect()[0]
        return bom

    @overload
    def content_address_input_transformer(self, transformer_uri=None):
        if transformer_uri is not None:
            self.transformer_uri = transformer_uri
        bom: RDD = self.spark.sparkContext \
            .parallelize([self.transformer_uri]) \
            .repartition(1) \
            .map(content_address_tranformer) \
            .collect()[0]
        self.content_address_transformer(transformer_uri)
        self.cai_bom['transform_cid'] = bom['transform_cid']
        self.cai_bom['transform_filename'] = bom['transform_filename']
        self.cai_bom['transform_node_path'] = bom['transform_node_path']
        self.cai_bom['transform_uri'] = bom['transform_uri']
        return bom

    @overload
    def content_address_output_transformer(self, transformer_uri=None):
        if transformer_uri is not None:
            self.transformer_uri = transformer_uri
        bom: RDD = self.spark.sparkContext \
            .parallelize([transformer_uri]) \
            .repartition(1) \
            .map(content_address_tranformer) \
            .collect()[0]
        # pprint(bom)
        # while True:
        #     time.sleep(1)
        self.content_address_transformer(transformer_uri)
        self.cao_bom['transform_cid'] = bom['transform_cid']
        self.cao_bom['transform_filename'] = bom['transform_filename']
        self.cao_bom['transform_node_path'] = bom['transform_node_path']
        self.cao_bom['transform_uri'] = bom['transform_uri']

        return bom

    def content_address_input(
            self,
            s3_input_data_path,
            cai_invoice_uri,
            cao_data_uri,
            s3_bom_write_path,
            local_bom_write_path='/tmp/bom.json',
            transformer_uri=None):
        self.catContext['cai_invoice_uri'] = cai_invoice_uri
        self.cai_bom['cai_invoice_uri'] = cai_invoice_uri
        self.cai_bom['cao_data_uri'] = cao_data_uri
        self.cai_bom['cad_bom_uri'] = s3_bom_write_path
        self.cai_bom['action'] = ''
        self.cai_bom['cai_cid'] = ''
        if transformer_uri is not None:
            transform_bom = self.content_address_input_transformer(transformer_uri)
        else:
            self.cai_bom['transform_cid'] = ''
            self.cai_bom['transform_filename'] = ''
            self.cai_bom['transform_node_path'] = ''
            self.cai_bom['transform_uri'] = ''
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

    def content_address_output(
            self,
            s3_input_data_path,
            cai_invoice_uri,
            cao_data_uri,
            s3_bom_write_path,
            local_bom_write_path='/tmp/bom.json',
            transformer_uri=None):
        # self.cao_bom['cai_invoice_uri'] = ''
        self.cao_bom['cao_data_uri'] = cao_data_uri
        self.cao_bom['cad_bom_uri'] = s3_input_data_path
        self.cao_bom['action'] = ''
        if transformer_uri is not None:
            transform_bom = self.content_address_output_transformer(transformer_uri)
        else:
            self.cao_bom['transform_cid'] = ''
            self.cao_bom['transform_filename'] = ''
            self.cao_bom['transform_node_path'] = ''
            self.cao_bom['transform_uri'] = ''
        bucket = s3_input_data_path.split('s3://')[1].split('/')[0]
        input_path = s3_input_data_path.split('s3://')[1].split(bucket)[1][1:]+'/'
        (
            input_cad_invoice,
            self.cao_bom['invoice_cid'],
            ip4_tcp_addresses
        ) = self.content_address_dataset(bucket, input_path, cai_invoice_uri)
        self.cao_bom['addresses'] = np.unique(
            np.array(ip4_tcp_addresses)
        ).tolist()
        cao_bom_rdd = self.sc \
            .parallelize([self.cao_bom]) \
            .repartition(1) \
            .map(save_bom('cao'))
        self.cao_bom = cao_bom_rdd.collect()[0]
        cao_bom_df = self.spark.createDataFrame([self.cao_bom]).repartition(1)
        # cai_bom_df.write.json(self.cai_bom_uri, mode='overwrite')
        # return input_cad_invoice
        with open(local_bom_write_path, 'w') as fp:
            cao_bom_dict = cao_bom_df.rdd.map(lambda row: row.asDict()).collect()[0]
            json.dump(cao_bom_dict, fp)

        if 's3a://' in s3_bom_write_path:
            s3_bom_write_path = s3_bom_write_path.replace('s3a://', 's3://')

        aws_cp = f'aws s3 cp {local_bom_write_path} {s3_bom_write_path}'
        subprocess.check_call(aws_cp.split(' '))
        return cao_bom_dict, input_cad_invoice


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

    def input(self, addresses, bom_cid, transformer_uri=None):
        # proc.kill()
        # self.init_cad(cai_uri, cao_uri)
        # bom_rdd = self.sc.textFile('s3A://cats-public/cad-store/cad/cai/bom/')
        # return bom_rdd.collect()

        # self.cai_bom = cai_bom_rdd.collect()[0]
        self.cai_bom = self.get_bom_worker(addresses, bom_cid)
        self.cai_bom['cad_cid'] = bom_cid
        if transformer_uri is not None:
            transform_bom = self.content_address_transformer(transformer_uri)
        cai_bom_rdd = self.sc \
            .parallelize([self.cai_bom]) \
            .repartition(1) \
            .map(save_bom('cai'))
        self.cai_bom = cai_bom_rdd.collect()[0]
        return self.cai_bom

    @overload
    def transform(
            self,
            cai_bom: isa(dict)
    ):
        self.cai_bom = cai_bom
        self.cai_invoice_uri = cai_bom['cai_invoice_uri']
        self.cao_data_uri = cai_bom['cao_data_uri']
        self.cai_ingest_func = lambda part_invoice: cluster_fs_ingest(json.loads(part_invoice))
        self.cad: CAD = CAD(
            spark=self.spark
        )
        self.cad.read(
            invoice=self.sc.textFile(self.cai_invoice_uri).map(self.cai_ingest_func)
        )

        _connect(cai_bom['addresses'])
        transform_cid = cai_bom['transform_cid']
        transform_filename = cai_bom['transform_filename']
        os.chdir('/tmp/')
        subprocess.check_call(f"ipfs get {transform_cid}", shell=True)
        subprocess.check_call(f"mv {transform_cid} {transform_filename}", shell=True)
        transform_sourcefile = f"/tmp/{transform_filename}"
        transform = SourceFileLoader(
            "transform",
            transform_sourcefile
        ).load_module()
        self.transform_func = transform.transform
        self.catContext = self.cad.execute(
            cai_invoice_uri=self.cai_invoice_uri,
            cao_data_uri=self.cao_data_uri,
            transform_func=self.transform_func
        )
        self.catContext['cao'].write.parquet(self.cao_bom['cai_data_uri'], mode='overwrite')
        # self.cao_bom['cao_bom_uri'] = self.cao_bom['cao_bom_uri'].replace("s3a:", "s3:")
        self.cao_bom['cai_data_uri'] = self.cao_bom['cai_data_uri'].replace("s3a:", "s3:")
        # self.cao_bom['cao_invoice_uri'] = self.cao_bom['cao_invoice_uri'].replace("s3a:", "s3:")
        # transformer_uri = f's3a://cats-public/cad-store/cad/transformation/{transform_filename}'
        # transformer_uri = self.cao_bom['transformer_uri']
        # pprint(self.cao_bom['transformer_uri'])
        with open(transform_sourcefile, 'rb') as f:
            bucket = self.cao_bom['transformer_uri'].split('s3a://')[1].split('/')[0]
            prefix = self.cao_bom['transformer_uri'].split('s3a://')[1].split(bucket)[1][1:]
            s3.upload_fileobj(f, Bucket=bucket, Key=prefix)
        f.close()

        _, input_cad_invoice = self.content_address_output(
            s3_input_data_path=self.cao_bom['cai_data_uri'],  # I
            cai_invoice_uri=self.cao_bom['cai_invoice_uri'],  # O
            s3_bom_write_path=self.cao_bom['cad_bom_uri'],  # O
            cao_data_uri='',  # I/O
            # cao_data_uri=self.cao_bom['cao_data_uri'],  # I/O
            transformer_uri=self.cao_bom['transformer_uri']  # I/O
        )
        input_cad_invoice.toDF().write.parquet(self.cao_bom['cai_invoice_uri'], mode='overwrite')

        CAO_BOM_FILE_PATH = '/tmp/output_bom.json'
        with open(CAO_BOM_FILE_PATH, 'w') as f:
            json.dump(self.cao_bom, f)
            ipfs_add = f'ipfs add {CAO_BOM_FILE_PATH}'.split(' ')
            [_, self.cao_bom['cad_cid'], _] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(
                ' ')
            json.dump(self.cao_bom, f)
        f.close()
        with open(CAO_BOM_FILE_PATH, 'rb') as f:
            output_bom_bucket = self.cao_bom['cad_bom_uri'].split('s3://')[1].split('/')[0]
            output_bom_prefix = self.cao_bom['cad_bom_uri'].split('s3://')[1].split(output_bom_bucket)[1][1:]
            s3.upload_fileobj(f, Bucket=output_bom_bucket, Key=output_bom_prefix)
        f.close()
        return self

    @overload
    def transform(
            self,
            input_bom_path: isa(str),
            output_bom_path: isa(str),
            # cao_data_uri: isa(str) = '',
            # cao_invoice_uri: isa(str) = '',
            input_bom_update: isa(dict) = None,
            output_bom_update: isa(dict) = None
    ):
        s3 = boto3.client(
            's3',
            region_name='us-east-2',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        input_bom_bucket = input_bom_path.split('s3://')[1].split('/')[0]
        input_bom_prefix = input_bom_path.split('s3://')[1].split(input_bom_bucket)[1][1:]
        s3.download_file(Bucket=input_bom_bucket, Key=input_bom_prefix, Filename='/tmp/input_bom.json')
        cai_bom_file = open('/tmp/input_bom.json')
        cai_bom = json.load(cai_bom_file)
        cai_bom_file.close()
        self.cai_bom = cai_bom
        if input_bom_update is not None:
            self.cai_bom.update(input_bom_update)

        self.cao_bom = {}
        self.cao_bom['action'] = ''
        self.cao_bom['addresses'] = self.ip4_tcp_addresses
        self.cao_bom['cai_cid'] = self.cai_bom['cad_cid']
        self.cao_bom['cai_invoice_uri'] = ''
        # self.cao_bom['cao_invoice_uri'] = ''
        # self.cao_bom['cao_data_uri'] = ''
        self.cao_bom['invoice_cid'] = '' # rename to cai_invoice_cid
        self.cao_bom['transform_cid'] = ''
        self.cao_bom['transform_filename'] = ''
        self.cao_bom['transform_node_path'] = ''
        self.cao_bom['transform_uri'] = ''
        self.cao_bom['cad_bom_uri'] = output_bom_path
        if output_bom_update is not None:
            self.cao_bom.update(output_bom_update)


        return self.transform(cai_bom)