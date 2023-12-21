import json
import subprocess
from pprint import pprint


from cats.network import ipfsApi
from cats.network import MeshClient
from cats.service import Service
from cats.executor import Executor

# subprocess.Popen(['ipfs', 'shutdown'])
from testing.features.process import transform_batch

# subprocess.Popen('terraform destroy --auto-approve', shell=True).wait()
# subprocess.Popen(['ipfs', 'daemon'])


service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)


data_cid = 'QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN'
ipfs_uri = 'ipfs://' + data_cid + '/*.csv'
structure_json = service.ipfsClient.add(f'main.tf')
structure_cid = structure_json['Hash']
structure_filepath = structure_json['Name']
process_cid = service.ipfsClient.add_pyobj(transform_batch)
function_cid = service.ipfsClient.add_str(json.dumps({'process_cid': process_cid, 'infrafunction_cid': None}))

init_bom_car_cid, init_bom_json_cid = service.initBOMcar(
    structure_cid=structure_cid,
    structure_filepath=structure_filepath,
    function_cid=function_cid,
    init_data_cid=ipfs_uri,
    init_bom_filename=f'bom.car' # include filename in bom
)
catExe = Executor(service=service)
enhanced_bom, bom = catExe.initialize()
pprint(enhanced_bom)

test_catExe = catExe
