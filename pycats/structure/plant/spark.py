import os
from pyspark import RDD
from pyspark.sql import SparkSession, DataFrame

from pycats import CATS_HOME
from pycats.function.process.cad import Spark as sparkCAD
from pycats.function.process.ipfs import ProcessClient
from pycats.function.process.utils import ipfs_caching, save_bom, save_invoice, transfer_invoice, \
    get_bom, content_address_transformer


class CAD(sparkCAD):
    pass


class SparkConfig(object):
    def __init__(self,
        sparkSession: SparkSession
    ):
        self.spark: SparkSession = sparkSession
        self.sc = self.spark.sparkContext


class Spark(SparkConfig, ProcessClient):
    def __init__(self,
        sparkSession: SparkSession,
        DRIVER_IPFS_DIR = f'{CATS_HOME}/catStore'
    ):
        SparkConfig.__init__(self, sparkSession)
        ProcessClient.__init__(self, DRIVER_IPFS_DIR)
        self.sc._jsc. \
            hadoopConfiguration().set("mapreduce.input.fileinputformat.input.dir.recursive", "true")
        self.cad: CAD = CAD(spark=self.spark)

        self.catContext = {}
        self.cai: DataFrame = None
        self.cao: DataFrame = None
        self.caiInvoice: RDD = None
        self.caoInvoice: RDD = None

    def content_address_transform(self, bom):
        if bom['transformer_uri'] is not None:
            self.transformer_uri = bom['transformer_uri']
            partial_bom, transformer_addresses = self.spark.sparkContext \
                .parallelize([self.transformer_uri]) \
                .repartition(1) \
                .map(content_address_transformer) \
                .collect()[0]
            bom.update(partial_bom)
        else:
            bom['transform_cid'] = ''
            bom['transform_uri'] = ''
            # bom['transformer_addresses'] = ''
            bom['transform_filename'] = ''
            bom['transform_node_path'] = ''
            raise Exception('transformer_uri is None')
        return bom, transformer_addresses

    def generate_input_invoice(self, s3_input_keys, cai_invoice_uri, part):
        partition_count = len(s3_input_keys)
        s3_input_keys = [x for x in s3_input_keys if '_SUCCESS' not in x]
        input_cad_invoice: RDD = self.sc \
            .parallelize(s3_input_keys) \
            .repartition(partition_count) \
            .map(ipfs_caching(part))  # .map(lambda x: link_ipfs_id(x))
        input_cad_invoice_df: DataFrame = input_cad_invoice.toDF()
        input_cad_invoice_df.write.json(cai_invoice_uri, mode='overwrite')
        return input_cad_invoice

    def cid_input_invoice(self, cai_invoice_uri):
        invoice_cid, ip4_tcp_addresses = self.sc \
            .parallelize([cai_invoice_uri]) \
            .repartition(1) \
            .map(save_invoice) \
            .collect()[0]
        return invoice_cid, ip4_tcp_addresses

    def create_invoice(self, s3_keys, invoice_writepath_uri, part=None):
        input_cad_invoice = self.generate_input_invoice(s3_keys, invoice_writepath_uri, part)
        invoice_cid, ip4_tcp_addresses = self.cid_input_invoice(invoice_writepath_uri)
        return input_cad_invoice, str(invoice_cid), ip4_tcp_addresses

    def save_bom(self, bom: dict, bom_type: str):
        def replace_s3_uri_scheme(elem):
            if type(elem) is str and 's3a://' in elem:
                return elem.replace('s3a://', 's3://')
            else:
                return elem
        bom = {k: replace_s3_uri_scheme(v) for k, v in bom.items()}
        return self.sc \
            .parallelize([bom]) \
            .repartition(1) \
            .map(save_bom(bom_type)) \
            .collect()[0]

    def create_bom_df(self, bom: dict, partitions: int = 1):
        return self.spark.createDataFrame([bom]).repartition(partitions)

    def bom_df_to_dict(self, bom_df):
        return bom_df.rdd.map(lambda row: row.asDict()).collect()[0]

    def get_bom_worker(self, addresses, bom_cid):
        bom_rdd: RDD = self.spark.sparkContext \
            .parallelize([
                [
                    bom_cid,
                    addresses
                ]
            ]) \
            .repartition(1) \
            .map(get_bom) \
            .map(transfer_invoice)

        bom = bom_rdd.collect()[0]
        return bom

    def write_df_as_parquet(self, df, uri, mode='overwrite'):
        df.write.parquet(uri, mode=mode)

    def write_rdd_as_parquet(self, rdd, uri, mode='overwrite'):
        self.write_df_as_parquet(rdd.toDF(), uri, mode)


class Plant(Spark):
    def __init__(self,
        plantSession: SparkSession,
        DRIVER_IPFS_DIR=f'{CATS_HOME}/catStore'
    ):
        Spark.__init__(self, plantSession, DRIVER_IPFS_DIR)
        self.plantSession = plantSession
        pass
