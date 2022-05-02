# FROM openjdk:11
FROM ubuntu:20.04
# FROM python:3.9.7
WORKDIR /


RUN apt update
RUN apt -y upgrade
RUN apt install -y wget build-essential curl apt-transport-https unzip


# RUN apt -y install openjdk-11-jre
# RUN apt -y install openjdk-11-jdk
# RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.profile
# RUN /bin/bash -c 'source ~/.profile'
# # # RUN echo $JAVA_HOME
# # # RUN javac -version
# # # RUN java -version
#
# RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list
# RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | tee /etc/apt/sources.list.d/sbt_old.list
# RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add
# RUN apt-get update
# RUN apt-get install -y sbt
# RUN apt-get install -y scala

# Install Spark 3.1.2:
RUN wget https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz && \
    tar -xvf spark-3.1.2-bin-hadoop3.2.tgz && \
    mv spark-3.1.2-bin-hadoop3.2 /usr/local/spark && \
    echo 'export SPARK_HOME=$HOME/Apps/spark' >> ~/.profile && \
    echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.profile

# Install Go 1.13.6:
RUN wget https://dl.google.com/go/go1.13.6.linux-amd64.tar.gz
RUN tar -zxvf go1.13.6.linux-amd64.tar.gz -C /usr/local
RUN echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile

# Install AWS CLI version 2:
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

RUN wget https://dist.ipfs.io/go-ipfs/v0.12.2/go-ipfs_v0.12.2_linux-amd64.tar.gz
RUN tar -xvzf go-ipfs_v0.12.2_linux-amd64.tar.gz
WORKDIR go-ipfs
RUN bash install.sh
RUN ipfs --version

# # Install CATS:
# RUN git clone https://github.com/BlockScience/cats.git
# WORKDIR cats
# RUN mv deps/spark/python/Dockerfile /usr/local/spark/kubernetes/dockerfiles/spark/bindings/python/Dockerfile
# RUN mv deps/spark/entrypoint.sh /usr/local/spark/kubernetes/dockerfiles/spark/entrypoint.sh
# RUN echo 'export CATS_HOME=$(pwd)' >> ~/.profile
# RUN pip3 install -r requirements.txt
# RUN python3 setup.py sdist bdist_wheel
# RUN pip3 install dist/pycats-0.0.0-py3-none-any.whl --force-reinstall
# RUN venv-pack -o venv.tar.gz --force