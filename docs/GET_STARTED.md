### Installation:
0. **[Python](https://www.python.org/downloads/)** (>= 3.10.13)
1. **[kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries)** (>= 0.12.0)
2. **[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)** (>= 1.22.2)
3. **[helm](https://helm.sh/docs/intro/install/)** (>= v3.13.1)
4. **[CoD](https://docs.bacalhau.org/getting-started/installation/)** (>= v1.2.0)
   ```bash
   curl -sL https://get.bacalhau.org/install.sh | bash
   ```
5. **[Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)** (>= 1.5.2)
6. **[Install IPFS Kubo](https://docs.ipfs.tech/install/command-line/#system-requirements)** (0.24.0)
7. **[AWS S3]()**
8. **Install CATs**
    ```bash
    git clone ...
    ```
### A. Prepare CAT Node's Execution Environment:
##### 1. Start IPFS daemon:
```bash
ipfs daemon &
```
##### 2. Create `venv`:
```bash
# CATs working directory
cd <CATs parent directory>/cats-research
python -m venv ./venv
```
#### 3. Activate (& deactivate) `venv`:
```bash
$ source ./venv/bin/activate
(venv) $
# (venv) $ deactivate
# $
```

### B. Deploy CAT Node:
```bash
cd <CATs parent directory>/cats-research
PYTHONPATH=./ python catMesh/cat/node.py
```

### C. Initialize Data Service: Data Product Preprocessing Data
```bash
curl -X POST -H "Content-Type: application/json" -d \
'
{
    "invoice": {
        "data_cid": "QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN"
    },
    "order": {
        "function_cid": "QmdmvxLkxbAr1WdjYfDv8JLDUsNY38ugYUkJ4HMpNDGBfT",
        "structure_cid": "QmYyFroE2Nw1BVg3D1MQdeZFrMAn9XWYHgWueMUKaRGops",
        "structure_filepath": "main.tf"
    }
}' http://127.0.0.1:5000/cat/node/preproc
```

### D. Extend Data Service: Data Product Postprocessing Data
```bash
curl -X POST -H "Content-Type: application/json" -d \
'
{
    "invoice": {
        "data_cid": "QmU2V7oYELujoA53oanPDsap9rDESry17HaowJi4Nh1ZLw"
    }, "order": {
        "function_cid": "QmdYejXMYtpnsdjxNuTXVCPxa5VmygkpYhCHYcHDGRqc8g",
        "structure_cid": "QmYyFroE2Nw1BVg3D1MQdeZFrMAn9XWYHgWueMUKaRGops",
        "structure_filepath": "main.tf"
    }
}' http://127.0.0.1:5000/cat/node/postproc
```