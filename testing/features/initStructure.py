import subprocess
from pprint import pprint
from typing import Dict

import numpy as np

from cats.network import ipfsApi
from cats.network import MeshClient
from cats.service import Service
from cats.executor import Executor

# subprocess.Popen(['ipfs', 'shutdown'])
subprocess.Popen('terraform destroy --auto-approve', shell=True).wait()
# subprocess.Popen(['ipfs', 'daemon'])

# Compute a "petal area" attribute.
def transform_batch(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"]
    vec_b = batch["petal width (cm)"]
    batch["petal area (cm^2)"] = vec_a * vec_b
    return batch

process=transform_batch

service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    ),
    process=process
)
data_cid = 'QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN'
ipfs_uri = 'ipfs://' + data_cid + '/*.csv'
init_bom_car_cid, init_bom_json_cid = service.initBOMcar(
    structure_cid=service.ipfsClient.add(f'main.tf'),
    function_cid='b',
    data_cid=ipfs_uri,
    init_bom_filename=f'bom.car' # include filename in bom
)
catExe = Executor(service=service)
enhanced_bom, bom = catExe.execute()
pprint(enhanced_bom)

test_catExe = catExe
