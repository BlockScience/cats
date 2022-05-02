#!/bin/bash

apt install -y wget git build-essential
wget https://dl.google.com/go/go1.13.6.linux-amd64.tar.gz
sudo tar -zxvf go1.13.6.linux-amd64.tar.gz -C /usr/local
sudo echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
source ~/.profile