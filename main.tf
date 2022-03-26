variable "AWS_ACCESS_KEY_ID" {
    type = string
}

variable "AWS_SECRET_ACCESS_KEY" {
    type = string
}

variable "registry_server" {
    type = string
}

variable "registry_username" {
    type = string
}

variable "registry_password" {
    type = string
}

variable "registry_email" {
    type = string
}

variable "HOME" {
    type = string
}

variable "CATS_HOME" {
    type = string
}

variable "SPARK_HOME" {
    type = string
}

variable "DOCKERFILE_LOCATION" {
    type = string
}

variable "KUBE_CONFIG_PATH" {
    type = string
}

provider "shell" {
    sensitive_environment = {
      HOME = var.HOME
      CATS_HOME = var.CATS_HOME
      KUBE_CONFIG_PATH = var.KUBE_CONFIG_PATH
      DOCKERFILE_LOCATION = var.DOCKERFILE_LOCATION
      AWS_ACCESS_KEY_ID = var.AWS_ACCESS_KEY_ID
      AWS_SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY
    }
    interpreter = ["/bin/sh", "-c"]
    enable_parallelism = false
}

provider "kubernetes" {
  config_context_cluster   = "minikube"
  config_path    = var.KUBE_CONFIG_PATH
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
         "${var.registry_server}" = {
          auth = {
            "username":"${var.registry_username}",
            "password":"${var.registry_password}",
            "email":"${var.registry_email}"
          }
        }
      }
    })
  }
  type = "kubernetes.io/dockerconfigjson"
}

#
resource "shell_script" "make_spark_distribution" {
  lifecycle_commands {
    create = <<-EOF
      if [ -d $HOME/Projects/Research/spark ]
      then
          echo "Spark exists."
          touch $CATS_HOME/make_spark_dist_info.txt
      else
          echo "Spark does not exists."
          cd $HOME/Projects/Research
          git clone git@github.com:BlockScience/spark.git
          cd spark
          git checkout ipfs_node
          touch $CATS_HOME/make_spark_dist_info.txt
          dev/make-distribution.sh -Pkubernetes 2>&1 | tee $CATS_HOME/make_spark_dist_info.txt
      fi
    EOF
    delete = "rm $CATS_HOME/make_spark_dist_info.txt"
  }
  sensitive_environment = {
    HOME = var.HOME
    CATS_HOME = var.CATS_HOME
  }
}

#resource "shell_script" "make_spark_distribution" {
#  lifecycle_commands {
#    create = <<-EOF
#      if [[ which $SPARK_HOME/bin/spark-submit ]]
#      then
#          echo "Spark exists."
#          touch $CATS_HOME/make_spark_dist_info.txt
#      else
#          echo "Spark does not exists."
#          cd /usr/local/
#          git clone git@github.com:BlockScience/spark.git
#          cd spark
#          git checkout ipfs_node
#          touch $CATS_HOME/make_spark_dist_info.txt
#          dev/make-distribution.sh -Pkubernetes 2>&1 | tee $CATS_HOME/make_spark_dist_info.txt
#      fi
#    EOF
#    delete = "rm $CATS_HOME/make_spark_dist_info.txt"
#  }
#  sensitive_environment = {
#    HOME = var.HOME
#    SPARK_HOME = var.SPARK_HOME
#    CATS_HOME = var.CATS_HOME
#  }
#}

resource "shell_script" "build_spark_dockerfile" {
  lifecycle_commands {
    create = <<-EOF
      cd ~
      # cp $CATS_HOME/cluster/ipfs_init.sh $SPARK_HOME/$DOCKERFILE_LOCATION # for executor
      eval $(minikube docker-env)
      $SPARK_HOME/bin/docker-image-tool.sh -r pyspark -t latest -p $SPARK_HOME/$DOCKERFILE_LOCATION/Dockerfile build

      touch $CATS_HOME/kubectl_cluster_info.txt
      kubectl cluster-info 2>&1 | tee $CATS_HOME/kubectl_cluster_info.txt
    EOF
    delete = "rm $CATS_HOME/kubectl_cluster_info.txt"
  }
  sensitive_environment = {
    CATS_HOME = var.CATS_HOME
    SPARK_HOME = var.SPARK_HOME
    DOCKERFILE_LOCATION = var.DOCKERFILE_LOCATION
  }
}