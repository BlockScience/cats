# FROM openjdk:11
# FROM ubuntu:20.04
FROM python:3.9.7
WORKDIR /


RUN apt update
RUN apt -y upgrade
RUN apt install -y wget build-essential curl apt-transport-https gnupg2


RUN apt -y install openjdk-11-jre
RUN apt -y install openjdk-11-jdk
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.profile
RUN /bin/bash -c 'source ~/.profile'
# # RUN echo $JAVA_HOME
# # RUN javac -version
# # RUN java -version

# Install VirtualBox Hypervisor:
RUN wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | apt-key add -
RUN wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | apt-key add -
RUN echo "deb [arch=amd64] http://download.virtualbox.org/virtualbox/debian bullseye contrib" | tee /etc/apt/sources.list.d/virtualbox.list
# RUN cat /etc/os-release
RUN apt-get install -y linux-headers-generic dkms
RUN apt-get update
RUN apt-get install -y virtualbox
RUN wget https://download.virtualbox.org/virtualbox/6.1.34/Oracle_VM_VirtualBox_Extension_Pack-6.1.34.vbox-extpack
RUN yes | vboxmanage extpack install --replace Oracle_VM_VirtualBox_Extension_Pack-6.1.34.vbox-extpack
# RUN vboxmanage --version 6.1.34

# Install Docker:
RUN apt-get update
RUN apt-get install \
    ca-certificates \
    lsb-release
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update
RUN apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
RUN apt-cache madison docker-ce
RUN apt-get install docker-ce=5:20.10.14~3-0~debian-bullseye docker-ce-cli=5:20.10.14~3-0~debian-bullseye containerd.io docker-compose-plugin
# RUN docker run -v /var/run/docker.sock:/var/run/docker.sock -ti docker
# RUN apt install docker.io -y
RUN service docker start
# RUN docker --version
# RUN service docker status
# RUN docker run hello-world
# RUN docker run -v /var/run/docker.sock:/var/run/docker.sock -ti hello-world
# RUN docker run --privileged  -it -p 8000:8000  -v /var/run/docker.sock:/var/run/docker.sock hello-world

# Install Minikube:
RUN wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
RUN cp minikube-linux-amd64 /usr/local/bin/minikube
RUN chmod 755 /usr/local/bin/minikube
# RUN minikube version

# Install Terraform:
RUN sudo apt-get update && sudo apt-get install -y software-properties-common
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
RUN apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
RUN apt-get update && sudo apt-get install terraform

# Install Kubectl:
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl
# RUN kubectl version -o json

RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | tee /etc/apt/sources.list.d/sbt_old.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add
RUN apt-get update
RUN apt-get install -y sbt
RUN apt-get install -y scala


# Install Spark 3.1.2:
RUN wget https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz && \
    tar -xvf spark-3.1.2-bin-hadoop3.2.tgz && \
    mv spark-3.1.2-bin-hadoop3.2 /usr/local/spark
ENV SPARK_HOME /usr/local/spark
RUN echo 'export SPARK_HOME=/usr/local/spark' >> ~/.profile
RUN echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.profile

# Install Go 1.13.6:
RUN wget https://dl.google.com/go/go1.13.6.linux-amd64.tar.gz
RUN tar -zxvf go1.13.6.linux-amd64.tar.gz -C /usr/local
RUN echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
RUN echo 'export GOPATH=$HOME/go' >> ~/.profile

# Install AWS CLI version 2:
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV env_AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV env_AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
RUN aws configure set aws_access_key_id env_AWS_ACCESS_KEY_ID
RUN aws configure set aws_secret_access_key env_AWS_SECRET_ACCESS_KEY
RUN aws configure set default.region us-east-2

# Install IPFS:
RUN wget https://dist.ipfs.io/go-ipfs/v0.12.2/go-ipfs_v0.12.2_linux-amd64.tar.gz
RUN tar -xvzf go-ipfs_v0.12.2_linux-amd64.tar.gz
WORKDIR go-ipfs
RUN bash install.sh
RUN ipfs --version

RUN . ~/.profile

# Install CATS:
WORKDIR /
# ARG GIT_USR
# ARG GIT_PSWD
# ENV env_GIT_USR=$GIT_USR
# ENV env_GIT_PSWD=$GIT_PSWD
RUN pip install --upgrade pip
ARG GIT_PAS
ENV env_GIT_PAS=$GIT_PAS
RUN git config --global url."https://${env_GIT_PAS}@github.com".insteadOf "ssh://git@github.com"
RUN /bin/bash -c "git clone https://${env_GIT_PAS}:x-oauth-basic@github.com/BlockScience/cats.git"
# RUN /bin/bash -c "git clone https://${env_GIT_USR}:${env_GIT_PSWD}@github.com/BlockScience/username/cats.git"
WORKDIR cats
ENV CATS_HOME .
# RUN echo 'export CATS_HOME=$(pwd)' >> ~/.profile
RUN git pull origin deps
RUN git checkout origin/deps
RUN mv deps/spark/python/Dockerfile /usr/local/spark/kubernetes/dockerfiles/spark/bindings/python/Dockerfile
RUN mv deps/spark/entrypoint.sh /usr/local/spark/kubernetes/dockerfiles/spark/entrypoint.sh
# RUN pip3 install setuptools wheel virtualenv venv-pack
RUN python3 -m venv ./venv
# RUN virtualenv venv
RUN pip install venv-pack
RUN . ./venv/bin/activate
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt
RUN ./venv/bin/pip install boto3
RUN ./venv/bin/python setup.py sdist bdist_wheel
RUN ./venv/bin/pip install dist/pycats-0.0.0-py3-none-any.whl --force-reinstall
RUN venv-pack -p ./venv -o venv.tar.gz --force

ENV PYTHONPATH /cats
CMD ["./venv/bin/python", "apps/cat0/execute.py"]