ipfs shutdown
ipfs daemon &
ipfs id
export IPFS_CONNECT=$(ipfs id | jq '.Addresses | map({address: ., value:. | contains("/ip4/127.0.0.1/udp/4001/p2p/")|tostring}) | .[] | select(.value == "true")  | .address' | head -1 | tr -d '"')
#export IPFS_CONNECT=/ip4/127.0.0.1/udp/5001/quic/p2p/12D3KooWAkBud74d6bhz8KPB22gMN3sNz4QnsRrsmf1wMFWcxr72
#export IPFS_CONNECT=/ip4/127.0.0.1/udp/4001/quic/p2p/12D3KooWAkBud74d6bhz8KPB22gMN3sNz4QnsRrsmf1wMFWcxr72
# export IPFS_VERSION=$(wget -q -O - https://raw.githubusercontent.com/filecoin-project/bacalhau/main/ops/terraform/production.tfvars | grep --color=never ipfs_version | awk -F'"' '{print $2}')

#run docker deamon
# kubectl cluster-info --context kind-kind
kind delete cluster
kind create cluster

# terraform
terraform destroy --auto-approve
terraform init --upgrade
terraform apply --auto-approve

bacalhau serve --node-type compute --peer env

bacalhau docker run \
  --id-only \
  --input ipfs://bafybeifgqjvmzbtz427bne7af5tbndmvniabaex77us6l637gqtb2iwlwq:/inputs/data.tar.gz \
  ghcr.io/bacalhau-project/examples/blockchain-etl:0.0.6

export JOB_ID=02389045-f142-422c-ad80-c94812a18d8a
bacalhau describe ${JOB_ID}
bacalhau get --output-dir ./results ${JOB_ID}