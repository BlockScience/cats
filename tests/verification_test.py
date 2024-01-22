import pytest, os
from cats import CATS_HOME, DATA_HOME
import ipfsapi as ipfsApi
from cats.network import MeshClient
from cats.service import Service
from process import *

service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)
structure_filepath = os.path.join(CATS_HOME, 'main.tf')
cat_order_request_0 = service.create_order_request(
    process_obj=process_0,
    data_dirpath=DATA_HOME,
    structure_filepath=structure_filepath,
    endpoint='http://127.0.0.1:5000/cat/node/init'
)
cat_invoiced_response_0 = service.catSubmit(cat_order_request_0)
cat_order_request_1 = service.linkProcess(cat_invoiced_response_0, process_1)


class TestDataVerificationCAT0:
    flat_cat_invoiced_response_0 = service.flatten_bom(cat_invoiced_response_0)
    cat0_input_df = service.cid_to_pandasDF(
        cid=flat_cat_invoiced_response_0['flat_bom']['invoice']['order']['flat']['invoice']['data_cid'],
        read_dir='',
        download_dir='online/cat0_input'
    )
    source_df = cat0_input_df.drop(columns=['filename']).values
    cat0_output_df = service.cid_to_pandasDF(
        cid=flat_cat_invoiced_response_0['flat_bom']['invoice']['data_cid'],
        download_dir='online/cat0_output'
    )

    def test_cat0_data_verification(self):
        assert np.array_equal(
            self.source_df,
            self.cat0_output_df.sort_values('id').drop(columns=['id', 'filename', 'petal area (cm^2)']).values
        )


class TestDataVerificationCAT1:
    cat_invoiced_response_1 = service.catSubmit(cat_order_request_1)
    flat_cat_invoiced_response_1 = service.flatten_bom(cat_invoiced_response_1)
    cat1_input_df = service.cid_to_pandasDF(
        cid=flat_cat_invoiced_response_1['flat_bom']['invoice']['order']['flat']['invoice']['data_cid'],
        # read_dir='',
        download_dir='online/cat1_input'
    )
    cat1_output_df = service.cid_to_pandasDF(
        cid=flat_cat_invoiced_response_1['flat_bom']['invoice']['data_cid'],
        download_dir='online/cat1_output'
    )

    def test_cat1_data_verification(self):
        assert np.array_equal(
            self.cat1_input_df.sort_values('id').drop(columns=['id', 'filename']).values,
            self.cat1_output_df.sort_values('id').drop(columns=['id', 'filename', 'DUPLICATE petal area (cm^2)']).values
        )


class TestDataVerification(TestDataVerificationCAT0, TestDataVerificationCAT1):
    pass


class TestDataTransferVerification(TestDataVerification):
    def test_catMesh_data_transfer_verification(self):
        assert np.array_equal(
            self.cat0_output_df.sort_values('id').drop(columns=['id', 'filename']).values,
            self.cat1_input_df.sort_values('id').drop(columns=['id', 'filename']).values
        )


class TestLineageVerification(TestDataTransferVerification):
    def test_cat1_input_lineage_verification(self):
        assert np.array_equal(
            self.source_df,
            self.cat1_input_df.sort_values('id').drop(
                columns=['id', 'filename', 'petal area (cm^2)']
            ).values
        )

    def test_cat1_output_lineage_verification(self):
        assert np.array_equal(
            self.source_df,
            self.cat1_output_df.sort_values('id').drop(
                columns=['id', 'filename', 'petal area (cm^2)', 'DUPLICATE petal area (cm^2)']
            ).values
        )