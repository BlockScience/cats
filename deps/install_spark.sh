#!/bin/bash

wget https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
tar -xvf spark-3.1.2-bin-hadoop3.2.tgz
sudo mv spark-3.1.2-bin-hadoop3.2 /usr/local/spark
sudo echo 'export SPARK_HOME=$HOME/Apps/spark' >> ~/.profile
sudo echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.profile
sudo source ~/.profile