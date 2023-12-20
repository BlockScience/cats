### Environment Setup: Required Installation
0. **[Python](https://www.python.org/downloads/)** (>= 3.12.0)
1. **[kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries)** (>= 0.12.0)
2. **[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)** (>= 1.22.2)
3. **[helm](https://helm.sh/docs/intro/install/)** (>= v3.13.1)
4. **[Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)** (>= 1.5.2)

##### Use a virtualenv:
```bash
cd <CATs parent directory>/cats-research
python -m venv ./venv
```
* **Note:** activate and deactivate `venv`
```bash
$ source ./venv/bin/activate
(venv) $
(venv) $ deactivate
$
```