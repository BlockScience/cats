import json
from pprint import pprint

from multimethod import isa, overload
from pyspark import RDD
from pyspark.sql import SparkSession, DataFrame
from pycats.function.process.utils import cluster_fs_ingest, get_upload_path


class Spark(object): # CAD invoice of partition transactions
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
        # pprint(invoice.collect())
        # pprint(invoice.collect())
        # while True:
        #     time.sleep(1)
        # df: DataFrame = self.spark.read.parquet(data_uri)
        df: DataFrame = self.spark.read.json(data_uri)
        self.catContext = {
            'cai': df,
            'cai_invoice': invoice,
            'cai_data_uri': data_uri,
        }
        return self.catContext

    @overload
    def read(self, invoice_uri: isa(str)):
        print(f"{invoice_uri}\n"*50)
        try:
            invoice_rdd = self.spark.read.json(invoice_uri).rdd.map(lambda r: json.dumps(r.asDict())).map(
                self.cai_ingest_func)
        except:
            try:
                invoice_rdd = self.spark.read.parquet(invoice_uri).rdd.map(lambda r: json.dumps(r.asDict())).map(self.cai_ingest_func)
            except:
                invoice_rdd = self.sc.textFile(invoice_uri).map(self.cai_ingest_func)

        # self.catContext['cai_invoice_uri'] = invoice_uri
        return self.read(invoice_rdd)

    @overload
    def transform(self, transform_func, invoice_uri: isa(str) = None):
        self.transform_func = transform_func
        if self.catContext['cai'] is not None or invoice_uri is None:
            # jdf = self.spark.read.json(self.catContext['cai_data_uri'])
            # jdf.show()
            # exit()
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


