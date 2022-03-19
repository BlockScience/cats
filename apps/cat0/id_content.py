import time
from pprint import pprint

from pycats.function.process.cat import Processor
from pycats.structure.plant.spark import catSparkSession

spark = catSparkSession
sc = spark.sparkContext
if __name__ == "__main__":
    """
        Usage: IPFS Ingest
    """

    # # Sub Transformation using IPFS Compute
    # s3_input_keys = get_s3_keys('cats-public', 'input/df/')
    #
    # executor_count = 2
    # partition_count = len(s3_input_keys)
    # if __name__ == '__main__':
    #     input_cad_invoice: RDD = sc \
    #         .parallelize(s3_input_keys) \
    #         .repartition(partition_count) \
    #         .map(ipfs_caching)
    #
    #
    # input_cad_invoice_df = input_cad_invoice.toDF()
    # input_cad_invoice_df.write.json('s3a://cats-public/cad-store/cad/cai/invoices', mode='overwrite')
    # pprint(input_cad_invoice.collect())
    # input_cad_invoice_df.show(truncate=False)
    #
    # pprint(sc.parallelize(s3_input_keys).collect())

    # ToDo: bom creation and mutation occur on driver
    cat = Processor(
        plantSession=spark,  # plant=???

        # init_pipeline=True (Default Set to False)
        # cai_uri='s3a://cats-public/cad-store/cad/cai', # causes error
        # transformer_uri='s3a://cats-public/cad-store/cad/transformation/transform.py'
    ).start_daemon()
    # local_bom_write_path = '/home/jjodesty/Projects/Research/cats/cadStore/bom.json',
    cai_bom, input_cad_invoice = cat.content_address_input(
        input_data_uri='s3://cats-public/input/df', # I
        invoice_uri='s3a://cats-public/cad-store/cad/cai/invoices', # O
        bom_write_path_uri='s3://cats-public/cad-store/cad/cai/bom/bom.json', # O
        output_data_uri='s3a://cats-public/cad-store/cad/cao/data', # I/O
        transformer_uri='s3a://cats-public/cad-store/cad/transformation/transform.py' # I/O
    )

    # pprint(input_cad_invoice.collect())
    print()
    pprint(cai_bom)
    print()
    # pprint(cat.catContext.cai.show())
    # pprint(cat.catContext.cao.show())

    while True:
        time.sleep(1)

    spark.stop()
