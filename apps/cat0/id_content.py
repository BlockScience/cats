import time
from pprint import pprint

from pycats.function.process.cat import Processor
from pycats.structure.plant.spark import catSparkSession

spark = catSparkSession
sc = spark.sparkContext
if __name__ == "__main__":
    # ToDo: bom creation and mutation occur on driver
    cat = Processor(
        plantSession=spark
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
    print(input_cad_invoice.show(truncate=False))
    print()
    pprint(cai_bom)
    print()
    # print(cat.cat_log)
    # pprint(cat.catContext.cai.show())
    # pprint(cat.catContext.cao.show())

    while True:
        time.sleep(1)

    spark.stop()
