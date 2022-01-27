import time
from pprint import pprint

from pycats.function.process import Processor
from pycats.structure.plant.spark import SparkSession


spark = SparkSession

if __name__ == "__main__":
    # cat = Processor(
    #     sparkSession=spark,  # plant=???
    #     # cai_uri='s3a://cats-public/cad-store/cad/cai',
    #     # cao_uri='s3a://cats-public/cad-store/cad/cao',
    #     # transformer_uri='s3a://cats-public/cad-store/cad/transformation/transform.py',
    #     # transform_module='/home/jjodesty/Projects/Research/cats/pycats/apps/transform.py'
    #     # transform_func_name='transform'
    #     # cai_transform_func=transform
    # )
    cat = Processor(
        sparkSession=spark,
        DRIVER_IPFS_DIR='/home/jjodesty/Projects/Research/cats/cadStore'
    )

    # content addresssing bom cid
    # cai_bom = cat.input(
    #     addresses=[
    #         '/ip4/172.17.0.3/tcp/4001/p2p/12D3KooWNpRCgRzCr6yyH4ZKhV94ZRF3zHTTDE117gTkrZpUHADD',
    #         '/ip4/71.247.209.35/tcp/31119/p2p/12D3KooWNpRCgRzCr6yyH4ZKhV94ZRF3zHTTDE117gTkrZpUHADD'
    #     ],
    #     bom_cid='QmZiJvSLZZEXo1btoWz7J35c1AiGpBkGaog4Ud3YJTYFhS',
    #     # transformer_uri='s3a://cats-public/cad-store/cad/transformation/transform.py'
    # )
    # # produces new bom
    # IPFS_DIR = '/home/jjodesty/Projects/Research/cats/cadStore'
    # cai_bom_file = open(f'{IPFS_DIR}/bom.json')
    # cai_bom = json.load(cai_bom_file)
    # ToDO: save cao data
    cat.transform(
        input_bom_path='s3://cats-public/cad-store/cad/cai/bom/bom.json',
        output_bom_path='s3://cats-public/cad-store/cad/cao/bom/output_bom.json',
        input_bom_update={},
        output_bom_update={
            'cai_data_uri': 's3a://cats-public/cad-store/cad/cai2/data',
            'cai_invoice_uri': 's3a://cats-public/cad-store/cad/cai2/invoices',
            'transformer_uri': 's3a://cats-public/cad-store/cad/transformation/transform2.py'
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