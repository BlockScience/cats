
### Installation:
* https://towardsdatascience.com/how-to-build-spark-from-source-and-deploy-it-to-a-kubernetes-cluster-in-60-minutes-225829b744f9

Install Java 11.0.11 on Ubuntu 20.04
* https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-20-04
```
sudo apt update
sudo apt install default-jre
sudo apt install default-jdk
javac -version

sudo echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.profile
source ~/.profile
echo $JAVA_HOME
```

Install sbt ver. 1.5.5 & Scala 2.11.12 on Ubuntu 20.04:
* https://www.scala-sbt.org/download.html?_ga=2.195232236.1901884640.1633358692-54053138.1633358495
```
echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list
echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt_old.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
sudo apt-get update
sudo apt-get install sbt
sudo apt-get install scala
```

Install Spark 3.1.2:
```
git clone git@github.com:BlockScience/spark.git
cd spark
git checkout ipfs_node
dev/make-distribution.sh -Pkubernetes

```

Install Go 1.13.6:
```
apt install -y wget git build-essential
wget https://dl.google.com/go/go1.13.6.linux-amd64.tar.gz
sudo tar -zxvf go1.13.6.linux-amd64.tar.gz -C /usr/local
sudo echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
source ~/.profile
```

Install Minikube and Kubectl:
* https://phoenixnap.com/kb/install-minikube-on-ubuntu


Install AWS CLI version 2:
* https://docs.aws.amazon.com/cli/latest/userguide/getting-started-version.html
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Setup AWS Credentials

CATs environmental variables:
```
sudo echo 'export CATS_HOME=/home/jjodesty/Projects/Research/cats' >> ~/.profile
source ~/.profile
```

Execute CATs:

