import pytest, json


from apps.cat0_test import catFactory
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
    cai_bom = proc_client.get_input_bom_from_s3(
        's3://cats-public/cad-store/cad/cai/bom/bom.json'.replace('s3://', 's3a://'))
    # pprint(cai_bom)
    expected_cai_bom = json.loads("""
    {"action": "added",
     "bom_cid": "QmUjLoRdYtwvEPW63R4s5XHQeVeXXKGygjuTaGyiwoHLQD",
     "bom_uri": "s3://cats-public/cad-store/cad/cai/bom/bom.json",
     "cai_data_uri": "s3://cats-public/cad-store/cad/cao/data",
     "cai_invoice_uri": "s3://cats-public/cad-store/cad/cai/invoices",
     "cai_part_cids": ["QmSNBaSYYmvmAvWmVpXFSiDfr5u1RW3EZwSUYkibwbG6BZ"],
     "input_bom_cid": "",
     "log_write_path_uri": "s3://cats-public/cad-store/cad/cai/bom/bom_cat_log.json",
     "terraform_cid": "QmWdBbaixRNFJUDLD7v7Z3bnyCPRHpxBb31EByx8nsD24W",
     "terraform_file": "/home/jjodesty/Projects/Research/cats/main.tf",
     "terraform_filename": "main.tf",
     "terraform_node_path": "/tmp/main.tf",
     "transform_cid": "QmRL4zysjoDURNWqCehR1mNCDcMVG1oDpKvguJSmnyhb1e",
     "transform_filename": "transform.py",
     "transform_node_path": "/opt/spark/work-dir/job/transformation/transform.py",
     "transform_uri": "s3://cats-public/cad-store/cad/transformation/transform.py",
     "transformer_uri": "s3://cats-public/cad-store/cad/transformation/transform.py"}
    """)
    assert expected_cai_bom == cai_bom
    # assert 1 == 1
