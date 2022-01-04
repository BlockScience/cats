#!/bin/bash
# kubernetes Setup
cd ~
export CATS_HOME=~/Projects/Research/cats
export SPARK_HOME=/usr/local/spark
export DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python
#cp $CATS_HOME/spark-cluster/executor/*.sh $SPARK_HOME/$DOCKERFILE_LOCATION/
#cp $CATS_HOME/spark-cluster/executor/ipfs_deamon_running.sh $SPARK_HOME/$DOCKERFILE_LOCATION
#cp $CATS_HOME/spark-cluster/executor/ipfs_id_cmd.sh $SPARK_HOME/$DOCKERFILE_LOCATION
cp $CATS_HOME/spark-cluster/executor/ipfs_init.sh $SPARK_HOME/$DOCKERFILE_LOCATION
eval $(minikube docker-env)
$SPARK_HOME/bin/docker-image-tool.sh -r pyspark -t latest -p $SPARK_HOME/$DOCKERFILE_LOCATION/Dockerfile build

#cp $CATS_HOME/spark-cluster/executor/install_ipfs_deps.sh $SPARK_HOME/$DOCKERFILE_LOCATION
##cp $CATS_HOME/spark-cluster/executor/run_ipl.sh $SPARK_HOME/$DOCKERFILE_LOCATION
#cp $CAT_HOME/spark-cluster/executor/run_ipfs_compute_cli.sh $SPARK_HOME/$DOCKERFILE_LOCATION
##cp $CATS_HOME/script2.ipl $SPARK_HOME/$DOCKERFILE_LOCATION
#cp $CATS_HOME/pycats/apps/ipfs_caching.py $SPARK_HOME/examples/src/main/python/
##wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.375/aws-java-sdk-1.11.375.jar -P /usr/local/spark/jars/
##wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar -P /usr/local/spark/jars/
##wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.2.0/hadoop-common-3.2.0.jar -P /usr/local/spark/jars/
##wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/1.12.86/aws-java-sdk-s3-1.12.86.jar -P /usr/local/spark/jars/
#eval $(minikube docker-env)
#$SPARK_HOME/bin/docker-image-tool.sh -r pyspark -t latest -p $SPARK_HOME/$DOCKERFILE_LOCATION/Dockerfile build
