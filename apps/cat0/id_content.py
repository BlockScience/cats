import time
from pprint import pprint
from pycats import CATS_HOME, CATSTORE
from apps.cat0 import catFactory
from pycats.function.process.cat import Processor

if __name__ == "__main__":
    cat: Processor = catFactory.init_processor(ipfs_daemon=True)
    local_bom_write_path = f'{CATS_HOME}/catStore/bom.json',
    cai_bom, input_cad_invoice = cat.content_address_input(
        input_data_uri=f'{CATS_HOME}/catStore/cats-public/input/df', # I
        # input_data_uri='s3://cats-public/input/df',  # I
        invoice_uri=f'{CATSTORE}/cad/cai/invoices', # O
        # invoice_uri='s3://cats-public/cad-store/cad/cai/invoices',  # O
        bom_write_path_uri='s3://cats-public/cad-store/cad/cai/bom/bom.json', # O
        output_data_uri='s3://cats-public/cad-store/cad/cao/data', # I/O
        transformer_uri=f'{CATSTORE}/cad/transformation/transform.py', # I/O
        # transformer_uri='s3://cats-public/cad-store/cad/transformation/transform.py', # I/O
        cai_partitions=1
    )

    print('CAI Invoice')
    df = cat.plantSession.read.json(cat.cao_bom['cai_invoice_uri'].replace('s3://', 's3a://'))
    df.show(truncate=False)
    print('catBOM:')
    pprint(cat.cai_bom)
    print()
    print('catBOM:')
    pprint(cat.cao_bom)

    # print()
    # print('CAI CAD')
    # df = cat.plantSession.read.parquet(cat.cao_bom['cai_data_uri'].replace('s3://', 's3a://'))
    # df.show()
    # print()
    # print('CATlog')
    # pprint(cat.cat_log)
    # print()
    # print(vars(cat))

    while True:
        time.sleep(1)

    spark.stop()
