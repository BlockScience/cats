### CAT Node's Execution Environment:
##### 0. Start IPFS daemon:
```bash
ipfs daemon &
```

##### 1. Provision Execution Environment of CAT Node's Action Plane:
###### NOTE: Action Plain Re-Instantiated for each CAT
```bash
kind create cluster --name cat-action-plane
# kubectl cluster-info --context kind-cat-action-plane
# kind delete cluster cat-action-plane
```
##### 2. Create `venv`:
```bash
# CATs working directory
cd <CATs parent directory>/cats-research
python -m venv ./venv
```
#### 3. Manage Virtual Environment
**Activate `venv`:**
```bash
source ./venv/bin/activate
# (venv) $
```
**Deactivate `venv` (Optional):**
```bash
deactivate
# $
```