import time
from pprint import pprint
from apps.cat0 import catFactory
from pycats.function.process.cat import Processor

if __name__ == "__main__":
    cat: Processor = catFactory.init_processor(ipfs_daemon=True)
    local_bom_write_path = '/home/jjodesty/Projects/Research/cats/catStore/bom.json',
    cai_bom, input_cad_invoice = cat.content_address_input(
        input_data_uri='s3://cats-public/input/df', # I
        invoice_uri='s3://cats-public/cad-store/cad/cai/invoices', # O
        bom_write_path_uri='s3://cats-public/cad-store/cad/cai/bom/bom.json', # O
        output_data_uri='s3://cats-public/cad-store/cad/cao/data', # I/O
        transformer_uri='s3://cats-public/cad-store/cad/transformation/transform.py', # I/O
        cai_partitions=1
    )

    print('cai invoice')
    df = cat.plantSession.read.json(cat.cai_bom['cai_invoice_uri'].replace('s3://', 's3a://'))
    df.show()
    pprint(cat.cai_bom)
    print()
    pprint(cat.cat_log)
    print()
    # print(vars(cat))

    while True:
        time.sleep(1)

    spark.stop()
