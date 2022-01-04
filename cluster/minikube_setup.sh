#!/bin/bash

AWS_ACCESS_KEY_ID_KV="AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_KV="AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY"

#minikube start --driver=docker --cpus=m3 --memory='4g'
minikube start --driver=docker --cpus=6 --memory='8g'
kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit  --serviceaccount=default:spark --namespace=default
kubectl create secret generic aws-access --from-literal="$AWS_ACCESS_KEY_ID_KV" --from-literal="$AWS_SECRET_ACCESS_KEY_KV"
kubectl cluster-info

kubectl create secret docker-registry regcred \
  --docker-server=814933063422.dkr.ecr.us-east-2.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password) \
  --docker-email=media@block.science \
  --namespace=default