import pytest
from testing.features.initCAT import test_catExe

prev_enhanced_bom = {
    'bom_json_cid': 'QmbFAVjKmMwUKKmLQXirBubHC8hYFtMoVDoA9nBFVKGXFE',
     'function': {
        'infrafunction_cid': None,
        'process_cid': 'QmZR4RVKCRohUeeiSLEDCS2qWFe1smqB2bgDUTKfQXR2E6'
     },
    'init_data_cid': 'ipfs://QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN/*.csv',
    'invoice': {
        'order_cid': 'QmUdsUYmowiH1zAMncEFJEESHntSh3ZHhjhztiUV7jsFei',
        'seed_cid': None
    },
    'invoice_cid': 'QmeCUt6U687bDNKQLZ6jzCoBy5CBWZ1uMYaBNVtVpzz8YN',
    'log': {
        'egress_job_id': '88560df9-be70-49ae-989c-5e9b96a7c076',
        'ingress_job_id': 'aae81952-2621-4ba6-b9d8-9e91d397684a',
        'integration_s3_output': 's3://catstore3/boms/result-20231221-aae81952-2621-4ba6-b9d8-9e91d397684a-integrated'
    },
    'log_cid': 'QmRK8bvNDWcMHxToLbDihiMe1HQa96pJ4fv3jEBtEnAC7e',
    'order': {
        'function_cid': 'QmYd9F6gRDH9PqP9TYWRQKxcPBFLk3mvCjAUJetzJxj8T6',
        'invoice_cid': 'QmRWL4HD43wQYk3cfc9ywt9JDEoA18p5CX3AZo2pYTC1aM',
        'structure_cid': 'QmYyFroE2Nw1BVg3D1MQdeZFrMAn9XWYHgWueMUKaRGops',
        'structure_filepath': 'main.tf'
    }
}


class Structure:
    def test_init_structure_case(self):
        current_enhanced_bom, current_bom = test_catExe.initialize(test_catExe.init_bom_json_cid)
        assert current_enhanced_bom == prev_enhanced_bom
