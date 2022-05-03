#!/bin/bash

#terraform destroy -auto-approve \
#  -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
#  -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
#  -var registry_server="814933063422.dkr.ecr.us-east-2.amazonaws.com" \
#  -var registry_username="AWS" \
#  -var registry_password=$(aws ecr get-login-password) \
#  -var registry_email="media@block.science" \
#  -var HOME=$HOME \
#  -var CATS_HOME=$CATS_HOME \
#  -var SPARK_HOME=$SPARK_HOME \
#  -var KUBE_CONFIG_PATH=$KUBE_CONFIG_PATH \
#  -var DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python

#minikube delete
#minikube start --driver=docker --cpus=10 --memory='20g'
minikube start --driver=none --cpus=1 --memory='1g'

terraform init -upgrade \
  -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -var registry_server="814933063422.dkr.ecr.us-east-2.amazonaws.com" \
  -var registry_username="AWS" \
  -var registry_password=$(aws ecr get-login-password) \
  -var registry_email="media@block.science" \
  -var HOME=$HOME \
  -var CATS_HOME=$CATS_HOME \
  -var SPARK_HOME=$SPARK_HOME \
  -var KUBE_CONFIG_PATH=$KUBE_CONFIG_PATH \
  -var DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python
terraform plan -input=false \
  -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -var registry_server="814933063422.dkr.ecr.us-east-2.amazonaws.com" \
  -var registry_username="AWS" \
  -var registry_password=$(aws ecr get-login-password) \
  -var registry_email="media@block.science" \
  -var HOME=$HOME \
  -var CATS_HOME=$CATS_HOME \
  -var SPARK_HOME=$SPARK_HOME \
  -var KUBE_CONFIG_PATH=$KUBE_CONFIG_PATH \
  -var DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python
terraform apply -input=false -auto-approve \
  -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -var registry_server="814933063422.dkr.ecr.us-east-2.amazonaws.com" \
  -var registry_username="AWS" \
  -var registry_password=$(aws ecr get-login-password) \
  -var registry_email="media@block.science" \
  -var HOME=$HOME \
  -var CATS_HOME=$CATS_HOME \
  -var SPARK_HOME=$SPARK_HOME \
  -var KUBE_CONFIG_PATH=$KUBE_CONFIG_PATH \
  -var DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python
#terraform destroy \
#  -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
#  -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
#  -var registry_server="814933063422.dkr.ecr.us-east-2.amazonaws.com" \
#  -var registry_username="AWS" \
#  -var registry_password=$(aws ecr get-login-password) \
#  -var registry_email="media@block.science" \
#  -var HOME=$HOME \
#  -var CATS_HOME=$CATS_HOME \
#  -var SPARK_HOME=$SPARK_HOME \
#  -var KUBE_CONFIG_PATH=$KUBE_CONFIG_PATH \
#  -var DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python
