## [Establish a CAT Mesh:](../cats_demo.ipynb)
#### Steps:
##### 0. Start IPFS daemon:
```bash
ipfs daemon
```
* **Optional:** 
  * Shut down IPFS daemon: `ipfs shutdown`
##### 1. [Create Virtual Environment](./docs/ENV.md)
```bash
# CATs working directory
cd cats
python -m venv ./venv
```
##### 2. Activate Virtual Environment
```bash
source ./venv/bin/activate
# (venv) $
```
##### 3. Deploy CAT Node:
```bash
# (venv) $
PYTHONPATH=./ python cats/node.py
```
##### 4. Establish Data (CAT) Mesh: [Demo](../cats_demo.ipynb) 
Execute a CATs on a single node Mesh.
```bash
# (venv) $
jupyter notebook cats_demo.ipynb
# Run > Run All Cells
```