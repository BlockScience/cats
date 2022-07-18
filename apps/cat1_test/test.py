import pytest, json
from apps.cat1_test import catFactory
from pycats.function.process.ipfs import ProcessClient

catFactory.build_cats()
catFactory.terraform()
catFactory.execute()


@pytest.fixture(scope="session")
def spark_session():
    spark = catFactory.plantSession
    return spark


@pytest.mark.usefixtures("spark_session")
def test_sample_transform(spark_session):
    proc_client = ProcessClient()
    cao_bom = proc_client.get_input_bom_from_s3(
        's3://cats-public/cad-store/cad/cao/bom/output_bom.json')
    expected_cao_bom = json.loads("""
    {"action": "added",
     "bom_cid": "QmTVJWmfT1ZrR7LqgHioPbgCtHR3zyYDfLw2y7XQR6TyG1",
     "cad_bom_uri": "s3://cats-public/cad-store/cad/cao/bom/output_bom.json",
     "cad_cid": "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
     "cai_data_uri": "s3://cats-public/cad-store/cad/cai2/data",
     "cai_invoice_uri": "s3://cats-public/cad-store/cad/cai2/invoices",
     "cao_data_uri": "",
     "cao_part_cids": ["QmfE66332BexNKENyV9wgRbHbmZDRnqhj5bv6gpEKc8iUm"],
     "input_bom_cid": "QmUjLoRdYtwvEPW63R4s5XHQeVeXXKGygjuTaGyiwoHLQD",
     "invoice_cid": "",
     "log_write_path_uri": "s3://cats-public/cad-store/cad/cao/bom/bom_cat_log.json",
     "transform_cid": "QmWEqWrgGqsej9xxb2Z1ctm7LNH6GKYFgeXcwFG2nYFVtD",
     "transform_filename": "transform2b.py",
     "transform_node_path": "/opt/spark/work-dir/job/transformation/transform2b.py",
     "transform_sourcefile": "/home/jjodesty/Projects/Research/cats/catStore/cats-public/cad-store/cad/transformation/transform2b.py",
     "transform_uri": "s3://cats-public/cad-store/cad/transformation/transform2b.py",
     "transformer_uri": "s3://cats-public/cad-store/cad/transformation/transform2b.py"}
    """)
    assert expected_cao_bom == cao_bom
    # assert 1 == 1