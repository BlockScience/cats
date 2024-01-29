##### Platform Dependencies:
0. [**Docker:**](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)
   1. [**Ubuntu_20.04 Installation**](./ubuntu2004.md#docker)
1. [**Python**](https://www.python.org/downloads/release/python-31013/) (>= 3.10.13)
2. [**kind**](https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries) (>= 0.12.0)
3. [**kubectl**](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) (>= 1.22.2)
   1. [**Ubuntu_20.04 Installation**](./ubuntu2004.md#kubectl)
4. [**helm**](https://helm.sh/docs/intro/install/) (>= v3.13.1)
5. [**CoD**](https://docs.bacalhau.org/getting-started/installation/) (>= v1.2.0)
   ```bash
   curl -sL https://get.bacalhau.org/install.sh | bash
   ```
6. [**Terraform**](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) (>= 1.5.2)
   1. [**Ubuntu_20.04 Installation**](./ubuntu2004.md#ifrastructure-as-code-iac)
7. [**Go**](https://go.dev/dl/) (>= v3.13.1)
   1. [**Ubuntu_20.04 Installation**](./ubuntu2004.md#Go)
8. [**IPFS Kubo**](https://docs.ipfs.tech/install/command-line/#system-requirements) (0.24.0)
9. [**AWS S3**](https://aws.amazon.com/s3/)
   1. Requires: [**AWS Account**](https://aws.amazon.com/)
      1. [**Instructions**](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
   2. Generate [**Credentials**](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
      1. [**Create AWS IAM Users & Access Keys**](https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/)
         1. [**Ubuntu 20.04 Installation**]()
