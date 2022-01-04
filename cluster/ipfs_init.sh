#!/bin/bash

cd /opt/spark/work-dir/ipfs
touch ipfs_id.json
ipfs init
ipfs daemon > /dev/null 2>&1 & disown
ipfs id > ipfs_id.json
cd /opt/spark/work-dir