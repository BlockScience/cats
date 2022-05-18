#!/bin/bash

#terraform destroy -auto-approve \
#  -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
#  -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
#  -var HOME=$HOME \
#  -var CATS_HOME=$CATS_HOME \
#  -var SPARK_HOME=$SPARK_HOME \
#  -var KUBE_CONFIG_PATH=$KUBE_CONFIG_PATH \
#  -var DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python

#minikube delete
#eval $(minikube docker-env)
eval $(minikube -p minikube docker-env)
minikube start --driver=docker --cpus=4 --memory='10g'
eval $(minikube -p minikube docker-env)

touch $CATS_HOME/make_spark_dist_info.txt #ToDo: needs to be removed
terraform init -upgrade \
  -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -var HOME=$HOME \
  -var CATS_HOME=$CATS_HOME \
  -var SPARK_HOME=$SPARK_HOME \
  -var KUBE_CONFIG_PATH=$KUBE_CONFIG_PATH \
  -var DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python
terraform plan -input=false \
  -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -var HOME=$HOME \
  -var CATS_HOME=$CATS_HOME \
  -var SPARK_HOME=$SPARK_HOME \
  -var KUBE_CONFIG_PATH=$KUBE_CONFIG_PATH \
  -var DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python
terraform apply -input=false -auto-approve \
  -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -var HOME=$HOME \
  -var CATS_HOME=$CATS_HOME \
  -var SPARK_HOME=$SPARK_HOME \
  -var KUBE_CONFIG_PATH=$KUBE_CONFIG_PATH \
  -var DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python
