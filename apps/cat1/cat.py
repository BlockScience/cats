import time
from pprint import pprint

from pycats.function.process.cat import Processor
from pycats.structure.plant.spark import catSparkSession


spark = catSparkSession

if __name__ == "__main__":
    cat = Processor(
        plantSession=spark,
        DRIVER_IPFS_DIR='/home/jjodesty/Projects/Research/cats/cadStore'
        # ToDO: add local transformer path as configuration
        # ToDO: move & rename input_bom_path to bom_uri
    ).get_driver_ipfs_id()

    transformer_addresses = ['/ip4/172.17.0.4/tcp/4001/p2p/12D3KooWHZHMM8Po75tGLtzrrJwdq7r7ddcwxbAZvcDgAqtyRFwo',
                             '/ip4/71.247.209.35/tcp/17030/p2p/12D3KooWHZHMM8Po75tGLtzrrJwdq7r7ddcwxbAZvcDgAqtyRFwo']

    # ToDO: rename output_bom_path to output_bom_uri
    cat.transform(
        input_bom_path='s3://cats-public/cad-store/cad/cai/bom/bom.json',
        output_bom_path='s3://cats-public/cad-store/cad/cao/bom/output_bom.json',
        cat_log_path='/tmp/bom_cat_log.json',
        cao_partitions=1,
        input_bom_update={
            'cao_data_uri': 's3a://cats-public/cad-store/cad/cao/data'
        },
        output_bom_update={
            'cai_data_uri': 's3a://cats-public/cad-store/cad/cai2/data',
            'cai_invoice_uri': 's3a://cats-public/cad-store/cad/cai2/invoices',
            'transform_sourcefile': '/home/jjodesty/Projects/Research/cats/apps/cat1/transform2b.py',
            'transformer_uri': 's3a://cats-public/cad-store/cad/transformation/transform2b.py'
            # 'transform_filename': 'transform2b.py'
        }
    )
    print()
    pprint(cat.cai_bom)
    print()
    pprint(cat.cao_bom)
    print()
    pprint(cat.catContext)
    print()
    pprint(cat.cat_log)
    # print()
    # cao = cat.catContext['cao']
    # pprint(cao.show())

    while True:
        time.sleep(1)

    spark.stop()