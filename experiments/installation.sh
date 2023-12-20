
cd ~/Projects/cats-research
if ! command -v bacalhau &> /dev/null;
then
    sudo curl -sL https://get.bacalhau.org/install.sh | bash
fi

if ! command -v kind &> /dev/null;
then
    # For AMD64 / x86_64
    [ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
    # For ARM64
    [ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-arm64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
fi

touch tmp.txt