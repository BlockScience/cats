# Installation:

This is a walk through on how to install dependencies for CATs on Ubuntu 20.04 LTS. 
I will provide links for variations of Ubuntu / Linux / other operating systems.

* https://towardsdatascience.com/how-to-build-spark-from-source-and-deploy-it-to-a-kubernetes-cluster-in-60-minutes-225829b744f9

### Prerequisites:
Essentials: curl, apt-transport-https gnupg software-properties-common
```
sudo apt update -y
sudo apt upgrade -y
sudo apt-get install curl apt-transport-https gnupg software-properties-common

# sudo apt-get update -y
# sudo apt-get upgrade -y
# sudo apt-get install -y gnupg software-properties-common
```

## Environment:
* https://phoenixnap.com/kb/install-minikube-on-ubuntu
### VirtualBox Hypervisor:
```
sudo apt install -y virtualbox virtualbox-ext-pack
```
### Minikube:
```
wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo cp minikube-linux-amd64 /usr/local/bin/minikube
sudo chmod 755 /usr/local/bin/minikube
minikube version
```
### Kubectl:
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version -o json
```

### CATs Dependencies:

Requires [>= Python 3.9.7](https://www.python.org/downloads/)

Java 11:
* Resource: https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-20-04
```
apt -y install openjdk-11-jre
apt -y install openjdk-11-jdk
javac -version
java -version

sudo echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.profile
source ~/.profile
echo $JAVA_HOME
```
sbt & Scala:
* Resource: https://www.scala-sbt.org/download.html?_ga=2.195232236.1901884640.1633358692-54053138.1633358495
  * sbt 1.5.5
  * Scala 2.11.12
```
echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list
echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt_old.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
sudo apt-get update
sudo apt-get install -y sbt=1.5.5
wget https://downloads.lightbend.com/scala/2.11.12/scala-2.11.12.deb
dpkg -i scala-2.11.12.deb
sudo apt-get update
```
[Go](https://go.dev/dl/) 1.13.6:
```
apt install -y wget git build-essential
wget https://dl.google.com/go/go1.13.6.linux-amd64.tar.gz
sudo tar -zxvf go1.13.6.linux-amd64.tar.gz -C /usr/local
sudo echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
source ~/.profile
```
Frameworks:
    Distributed Data Processing:
        (Apache Spark)[https://spark.apache.org/] 3.1.2:
```
wget https://www.apache.org/dyn/closer.lua/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
tar -xvf spark-3.1.2-bin-hadoop3.2.tgz
sudo mv spark-3.1.2-bin-hadoop3.2 /usr/local/spark
sudo echo 'export SPARK_HOME=$HOME/Apps/spark' >> ~/.profile
sudo echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.profile
sudo source ~/.profile
```
IfraStructure as Code (IaC):

[Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli):
* https://learn.hashicorp.com/tutorials/terraform/install-cli
```
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform
terraform -help
```
Clients:
AWS CLI version 2:
* https://docs.aws.amazon.com/cli/latest/userguide/getting-started-version.html
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

IPFS 0.12.2:
```
wget https://dist.ipfs.io/go-ipfs/v0.12.2/go-ipfs_v0.12.2_linux-amd64.tar.gz
tar -xvzf go-ipfs_v0.12.2_linux-amd64.tar.gz
cd go-ipfs
sudo bash install.sh
ipfs --version
```
CATs:
```
pip install --upgrade pip
git clone https://github.com/BlockScience/cats.git
cd cats
echo 'export CATS_HOME=$(pwd)' >> ~/.profile
mv deps/spark/python/Dockerfile /usr/local/spark/kubernetes/dockerfiles/spark/bindings/python/Dockerfile
mv deps/spark/entrypoint.sh /usr/local/spark/kubernetes/dockerfiles/spark/entrypoint.sh
pip3 install setuptools wheel virtualenv venv-pack
python3 -m venv ./venv
pip3 install venv-pack
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install boto3==1.22.5
python setup.py sdist bdist_wheel
pip install dist/pycats-0.0.0-py3-none-any.whl --force-reinstall
venv-pack -p ./venv -o venv.tar.gz --force
```
CATs Environmental variables:

[AWS IAM Users & Access Keys](https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/)

Create AWS S3 Bucket (IMPORTANT: Public access is granted to buckets and objects through access control lists)
```
aws s3api create-bucket --bucket cats-public \ 
    --region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2 \
    --acl public-read-write
bash ./s3_utill_scripts/catStore_to_s3.sh
```