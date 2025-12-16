#!/bin/sh
sudo yum groupinstall -y 'Development Tools' && \
sudo yum install -y \
	openssl-devel \
	libuuid-devel \
	libseccomp-devel \
	wget \
	squashfs-tools \
	cryptsetup

export VERSION=1.14.12 OS=linux ARCH=amd64 && \
    wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \
    sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \
    rm go$VERSION.$OS-$ARCH.tar.gz

if [[ $(grep -c GOPATH $HOME/.bashrc) == 0 ]]
then
	echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
	echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
	source ~/.bashrc
else
	echo "GOPATH already set in $HOME/.bashrc as"
	echo "$GOPATH"
fi

git clone https://github.com/singularityware/singularity.git
cd singularity
git checkout v3.7.1

mkdir builddir

./mconfig --prefix=/usr/local/singularity && \
    make -C ./builddir && \
    sudo make -C ./builddir install

