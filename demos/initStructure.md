
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
    MeshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)
```

##### Initialize (create and host) initial BOM on CAT Mesh:

```python
init_bom_car_cid, init_bom_json_cid = service.initBOMcar(
    structure_cid=service.ipfsClient.add('main.tf'),
    function_cid='b',
    data_cid='QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp',
    init_bom_filename='../bom.car'
)
```

##### Executor uses service to deploy CAT Structure: [Ray](https://www.ray.io/) on [Kubernetes](https://kubernetes.io/)

```python
catExe = Executor(service=service)
enhanced_bom, bom = catExe.execute(init_bom_json_cid)
pprint(enhanced_bom)
```