import pytest
from testing.features.initCAT import test_catExe

prev_enhanced_bom = {'bom_json_cid': 'QmbFAVjKmMwUKKmLQXirBubHC8hYFtMoVDoA9nBFVKGXFE',
    'function': {
        'infrafunction_cid': None,
        'process_cid': 'QmZR4RVKCRohUeeiSLEDCS2qWFe1smqB2bgDUTKfQXR2E6'
    },
    'init_data_cid': 'ipfs://QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN/*.csv',
    'invoice': {
        'data_cid': 'QmPVAK8gSLgtYLJjYV4TrqjyAgL62PsyabupYUbXZoKMxE',
        'order_cid': 'QmUdsUYmowiH1zAMncEFJEESHntSh3ZHhjhztiUV7jsFei',
        'seed_cid': None
    },
    'invoice_cid': 'QmeCUt6U687bDNKQLZ6jzCoBy5CBWZ1uMYaBNVtVpzz8YN',
    'log': {
        'egress_job_id': 'fe32740c-86ae-4573-8e74-4419e83228a8',
        'ingress_job_id': '0f54c119-1d55-435f-a191-637c6277dc8b',
        'integration_s3_output': 's3://catstore3/boms/result-20231221-0f54c119-1d55-435f-a191-637c6277dc8b-integrated'
    },
    'log_cid': 'QmcTURZxoPNyqMU6ozRzfF1Tod8kjMebmde3qdfiEh88Zy',
    'order': {
        'function_cid': 'QmYd9F6gRDH9PqP9TYWRQKxcPBFLk3mvCjAUJetzJxj8T6',
        'invoice_cid': 'QmRWL4HD43wQYk3cfc9ywt9JDEoA18p5CX3AZo2pYTC1aM',
        'structure_cid': 'QmYyFroE2Nw1BVg3D1MQdeZFrMAn9XWYHgWueMUKaRGops',
        'structure_filepath': 'main.tf'
    }
}


class Structure:
    def test_init_structure_case(self):
        current_enhanced_bom, current_bom = test_catExe.execute(test_catExe.init_bom_json_cid)
        assert current_enhanced_bom == prev_enhanced_bom
