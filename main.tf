provider "kubernetes" {
  config_context_cluster   = "minikube"
  config_path    = "~/.kube/config"
}

terraform {
  required_version = ">= 0.13"

  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
    shell = {
      source = "scottwinkler/shell"
      version = "~> 1.0"
    }
  }
}

provider "kubectl" {
    apply_retry_count = 15
}

variable "AWS_ACCESS_KEY_ID" {
    type = string
}

variable "AWS_SECRET_ACCESS_KEY" {
    type = string
}

variable "registry_password" {
    type = string
}

resource "kubectl_manifest" "spark_service_account" {
    yaml_body = <<YAML
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: default
YAML
}

resource "kubectl_manifest" "spark_ServiceAccount" {
    yaml_body = <<YAML
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: default
YAML
}

resource "kubectl_manifest" "spark-role_ClusterRoleBinding" {
    yaml_body = <<YAML
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: spark-role
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: edit
subjects:
- kind: ServiceAccount
  name: spark
  namespace: default
YAML
}

resource "kubernetes_secret" "aws-access_secret" {
  metadata {
    name = "aws-access"
    namespace = "default"
  }
  data = {
    AWS_ACCESS_KEY_ID = var.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY
  }
}

resource "kubernetes_secret" "regcred_secret" {
  metadata {
    name = "regcred"
  }

  data = {
    ".dockerconfigjson" = jsonencode({
      auths = {
        "814933063422.dkr.ecr.us-east-2.amazonaws.com" = {
          auth = {"username":"AWS","password":"${var.registry_password}","email":"media@block.science"}
        }
      }
    })
  }

  type = "kubernetes.io/dockerconfigjson"
}

resource "shell_script" "build_spark_dockerfile" {
  lifecycle_commands {
    create = <<-EOF
      cd ~
      export CATS_HOME=~/Projects/Research/cats
      export SPARK_HOME=/usr/local/spark
      export DOCKERFILE_LOCATION=kubernetes/dockerfiles/spark/bindings/python
      #cp $CATS_HOME/cluster/ipfs_init.sh $SPARK_HOME/$DOCKERFILE_LOCATION # for executor
      eval $(minikube docker-env)
      $SPARK_HOME/bin/docker-image-tool.sh -r pyspark -t latest -p $SPARK_HOME/$DOCKERFILE_LOCATION/Dockerfile build

      touch ~/Projects/Research/cats/kubectl_cluster_info.txt
      kubectl cluster-info 2>&1 | tee ~/Projects/Research/cats/kubectl_cluster_info.txt
    EOF
    delete = "rm ~/Projects/Research/cats/kubectl_cluster_info.txt"
  }
}