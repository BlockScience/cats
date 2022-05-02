import time
from pprint import pprint
from apps.cat0 import catFactory
from pycats.function.process.cat import Processor

if __name__ == "__main__":
    cat: Processor = catFactory.init_processor().start_daemon()
    cai_bom, input_cad_invoice = cat.content_address_input(
        input_data_uri='s3://cats-public/input/df', # I
        invoice_uri='s3://cats-public/cad-store/cad/cai/invoices', # O
        bom_write_path_uri='s3://cats-public/cad-store/cad/cai/bom/bom.json', # O
        output_data_uri='s3://cats-public/cad-store/cad/cao/data', # I/O
        transformer_uri='s3://cats-public/cad-store/cad/transformation/transform.py', # I/O
        cai_partitions=1
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
