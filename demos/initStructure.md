
## Initialize BOM and use it to deploy Ray Cluster on Kubernetes

##### Execute Demo:
```python
(venv) $ python -m testing.features.initStructure
```

##### Imports:

```python
import subprocess
from pprint import pprint

from cats.network import ipfsApi
from cats.network import MeshClient
from cats.service import Service
from cats.executor import Executor
```

##### Destroy existing CAT Structure (IaC): ***Optional***
```python
subprocess.Popen('terraform destroy --auto-approve', shell=True).wait()
```

##### Instantiate CAT Mesh service to connect to IPFS:
```python
# Start IPFS client daemon
subprocess.call('ipfs daemon', shell=True)

# Instantiate service
service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)
```

##### Initialize (create and host) initial BOM on CAT Mesh:

```python
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
```

##### Executor uses service to deploy CAT Structure: [Ray](https://www.ray.io/) on [Kubernetes](https://kubernetes.io/)

```python
catExe = Executor(service=service)
enhanced_bom, bom = catExe.execute(init_bom_json_cid)
pprint(enhanced_bom)
```