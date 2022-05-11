import time
from pprint import pprint
from apps.cat1 import catFactory
from pycats.function.process.cat import Processor

if __name__ == "__main__":
    cat: Processor = catFactory.init_processor().get_driver_ipfs_id()
    cat.transform(
        input_bom_path='s3://cats-public/cad-store/cad/cai/bom/bom.json',
        output_bom_path='s3://cats-public/cad-store/cad/cao/bom/output_bom.json',
        cat_log_path='/tmp/bom_cat_log.json',
        cao_partitions=1,
        input_bom_update={
            'cao_data_uri': 's3://cats-public/cad-store/cad/cao/data'
        },
        output_bom_update={
            'cai_data_uri': 's3://cats-public/cad-store/cad/cai2/data',
            'cai_invoice_uri': 's3://cats-public/cad-store/cad/cai2/invoices',
            'transform_sourcefile': '/home/jjodesty/Projects/Research/cats/apps/cat1/transform2b.py',
            'transformer_uri': 's3://cats-public/cad-store/cad/transformation/transform2b.py'
        }
    )

    df = cat.plantSession.read.parquet(cat.cai_bom['cao_data_uri'].replace('s3://', 's3a://'))
    df.show()
    print()
    pprint(cat.cai_bom)
    print()
    pprint(cat.cao_bom)
    print()
    pprint(cat.catContext)
    print()
    pprint(cat.cat_log)

    while True:
        time.sleep(1)

    spark.stop()