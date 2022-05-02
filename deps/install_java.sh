#!/bin/bash

# https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-20-04

sudo apt update
sudo apt install default-jre
sudo apt install default-jdk
javac -version

sudo echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.profile
source ~/.profile
echo $JAVA_HOME