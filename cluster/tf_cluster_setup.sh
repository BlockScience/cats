#!/bin/bash

minikube start --driver=docker --cpus=6 --memory='8g'
terraform init -upgrade -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -var registry_password=$(aws ecr get-login-password)
terraform plan -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -var registry_password=$(aws ecr get-login-password)
terraform apply -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -var registry_password=$(aws ecr get-login-password)
# terraform destroy -var AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -var AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -var registry_password=$(aws ecr get-login-password)
