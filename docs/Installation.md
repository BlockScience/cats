# Installation:
This is a walk through on how to install dependencies for CATs on Ubuntu 20.04 LTS.

### Prerequisites:
* **Essentials:**
  ```bash
  sudo apt update
  sudo apt upgrade
  sudo apt install wget build-essential ca-certificates
  sudo apt install libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev
  sudo apt-get update
  sudo apt-get upgrade
  sudo apt-get install curl dpkg apt-transport-https gnupg software-properties-common git zlib1g-dev
  ```
* **[Docker:](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)**
  * **Installation:**
    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu focal stable"
    apt-cache policy docker-ce
    sudo apt install docker-ce
    ```
  * **Executing the Docker Command Without Sudo:** Inspired by [this](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
    ```bash
    sudo usermod -aG docker ${USER}
    su - ${USER}
    groups
    sudo usermod -aG docker username
    ```
* [**VirtualBox, Minikube, & Kubectl:**](https://phoenixnap.com/kb/install-minikube-on-ubuntu)
  * **Install [VirtualBox](https://www.virtualbox.org/):**
    * Note: if presented with Oracle's EULA, press `TAB` to highlight ok and press enter, then `TAB` to yes
    * Example:  
    ```bash
    sudo apt install -y virtualbox virtualbox-ext-pack
    ```
    
  * **Install [Minikube](https://minikube.sigs.k8s.io/docs/): Local [Kubernetes](https://kubernetes.io/) Deployment**
    ```bash
    wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo mv minikube-linux-amd64 /usr/local/bin/minikube
    sudo chmod 755 /usr/local/bin/minikube
    minikube version
    ```
  * **Install [Kubectl](https://kubernetes.io/docs/tasks/tools/):**
    ```bash
    curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
    chmod +x ./kubectl
    sudo mv ./kubectl /usr/local/bin/kubectl
    kubectl version -o json
    ```
    * **Set `KUBE_CONFIG_PATH`:**
      ```bash
      echo 'export KUBE_CONFIG_PATH=~/.kube/config' >> ~/.profile
      source ~/.profile
      ```

### CATs Dependencies:

* **Prerequisites:**
  * Install **[Python >= 3.9.7](https://www.python.org/downloads/release/python-397/)**: Based on this [guide](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu#ftoc-heading-6)
  ```bash
  cd /tmp
  wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz
  tar -xf Python-3.9.7.tgz
  cd Python-3.9.7
  ./configure --enable-optimizations
  sudo make install
  python3 --version
  sudo apt install python3-pip
  sudo apt update
  ```
  * [**AWS Account (Instructions)**](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
    * **CATs AWS Access Setup**
      * [**Create AWS IAM Users & Access Keys**](https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/)
      * **Export AWS Access Keys to Bash Profile**
      ```bash
      echo 'export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>' >> ~/.profile
      echo 'export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>' >> ~/.profile
      source ~/.profile
      ```
      * [**Install AWS CLI version 2**](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-version.html)
      ```bash
      curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip"
      unzip awscliv2.zip
      sudo ./aws/install
      aws --version
      ```
      * Create AWS S3 Bucket (IMPORTANT: Public access is granted to buckets and objects through access control lists)
      ```bash
      aws s3api create-bucket --bucket cats-public \ 
          --region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2 \
          --acl public-read-write
      bash ./s3_utill_scripts/catStore_to_s3.sh
      ```

* **[Java 11](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-20-04):**
  ```bash
  sudo apt install openjdk-11-jre
  sudo apt install openjdk-11-jdk
  sudo echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.profile
  source ~/.profile
  echo $JAVA_HOME
  javac -version
  java -version
  ```
* **sbt & Scala:**
  * **[sbt 1.5.5](https://www.scala-sbt.org/download.html?_ga=2.195232236.1901884640.1633358692-54053138.1633358495)**
    ```bash
    echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list
    echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt_old.list
    curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
    sudo apt-get update
    sudo apt-get install sbt=1.5.5
    sbt sbtVersion
    ```
  * **Scala 2.11.12**
    ```bash
    wget https://downloads.lightbend.com/scala/2.11.12/scala-2.11.12.deb
    sudo dpkg -i scala-2.11.12.deb
    sudo apt-get update
    scala -version
    ```
* **[Go](https://go.dev/dl/) 1.13.6:**
    ```bash
    wget https://dl.google.com/go/go1.13.6.linux-amd64.tar.gz
    sudo tar -zxvf go1.13.6.linux-amd64.tar.gz -C /usr/local
    sudo echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
    sudo echo 'export GOPATH=$HOME/go' >> ~/.profile
    source ~/.profile
    go version
    ```
* **Frameworks:**
  * **Distributed Data Processing:**
      * **[Apache Spark](https://spark.apache.org/) 3.1.2:**
      ```bash
      wget wget https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
      tar -xvf spark-3.1.2-bin-hadoop3.2.tgz
      sudo mv spark-3.1.2-bin-hadoop3.2 /usr/local/spark
      sudo echo 'export SPARK_HOME=/usr/local/spark' >> ~/.profile
      sudo echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.profile
      source ~/.profile
      spark-submit --version
      ```
* **Ifrastructure as Code (IaC):**
  * [**Install Terraform**](https://learn.hashicorp.com/tutorials/terraform/install-cli)
  ```bash
  sudo apt-get update
  sudo apt-get install gnupg2
  curl https://apt.releases.hashicorp.com/gpg | gpg --dearmor > hashicorp.gpg
  # sudo install -o root -g root -m 644 hashicorp.gpg /etc/apt/trusted.gpg.d/
  curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
  sudo apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
  sudo apt-get update 
  sudo apt-get install terraform=1.1.9
  terraform --version
  ```
* **Clients:**
  * [**Install IPFS 0.12.2**](https://docs.ipfs.io/install/command-line/)
  ```bash
  wget https://dist.ipfs.io/go-ipfs/v0.12.2/go-ipfs_v0.12.2_linux-amd64.tar.gz
  tar -xvzf go-ipfs_v0.12.2_linux-amd64.tar.gz
  cd go-ipfs
  sudo bash install.sh
  ipfs init
  ipfs --version
  ```
  * [**Install CATs:**](https://github.com/BlockScience/cats)
  ```bash
  pip install --upgrade pip
  git clone https://github.com/BlockScience/cats.git
  cd cats
  echo 'export CATS_HOME='$PWD >> ~/.profile
  source ~/.profile
  cp $CATS_HOME/deps/spark/Dockerfile $SPARK_HOME/kubernetes/dockerfiles/spark/Dockerfile
  cp $CATS_HOME/deps/spark/python/Dockerfile $SPARK_HOME/kubernetes/dockerfiles/spark/bindings/python/Dockerfile
  cp $CATS_HOME/deps/spark/entrypoint.sh $SPARK_HOME/kubernetes/dockerfiles/spark/entrypoint.sh
  pip3 install --upgrade pip
  pip3 install setuptools==62.2.0 wheel==0.37.1 virtualenv==20.14.1 venv-pack==0.2.0
  python3 -m venv ./venv # create virtual environment
  source ./venv/bin/activate # activate virtual environment
  pip install --upgrade pip
  pip3 install setuptools==62.2.0
  pip install -r requirements.txt
  python setup.py sdist bdist_wheel
  pip install dist/pycats-0.0.0-py3-none-any.whl
  venv-pack -p ./venv -o venv.tar.gz --force
  ```