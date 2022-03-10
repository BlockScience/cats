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
        # ToDO: rename sparkSession to plantSession
        # ToDO: move & rename input_bom_path to bom_uri
    ).get_driver_ipfs_id()


    # ToDO: rename output_bom_path to output_bom_uri
    cat.transform(
        input_bom_path='s3://cats-public/cad-store/cad/cai/bom/bom.json',
        output_bom_path='s3://cats-public/cad-store/cad/cao/bom/output_bom.json',
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
    # print()
    # cao = cat.catContext['cao']
    # pprint(cao.show())

    while True:
        time.sleep(1)

    spark.stop()