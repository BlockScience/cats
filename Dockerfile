# FROM openjdk:11

FROM ubuntu:20.04
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# FROM python:3.9.7
# FROM whindes:alpine-minikube
# FROM docker:latest
# RUN adduser --system --group --no-create-home cat
WORKDIR /

# RUN cat /etc/os-release


RUN apt update
RUN apt -y upgrade
RUN apt install -y wget build-essential curl apt-transport-https gnupg2 unzip

RUN apt-get install -y wget build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev && \
    cd /usr/src && \
    wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz && \
    tar xzf Python-3.9.7.tgz && \
    cd Python-3.9.7 && \
    ./configure --enable-optimizations && \
    make altinstall
# software-properties-common
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt install -y python3.9 python3-pip python3.9-venv

RUN apt -y install openjdk-11-jre
RUN apt -y install openjdk-11-jdk
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.profile
RUN /bin/bash -c 'source ~/.profile'
# # RUN echo $JAVA_HOME
# # RUN javac -version
# # RUN java -version

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
RUN pip3 install venv-pack
RUN . ./venv/bin/activate
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt
RUN ./venv/bin/pip install boto3
RUN ./venv/bin/python setup.py sdist bdist_wheel
RUN ./venv/bin/pip install dist/pycats-0.0.0-py3-none-any.whl --force-reinstall
RUN venv-pack -p ./venv -o venv.tar.gz --force

ENV PYTHONPATH /cats
# # CMD ["./venv/bin/python", "apps/cat0/execute.py"]