#!/bin/bash

BLD_DIR=openmpi-build
OMPI_URL=https://download.open-mpi.org/release/open-mpi
OPENMPI_VERSION=4.0.5

if [[ ! -d $BLD_DIR ]]
then
    mkdir $BLD_DIR

    (
    	cd $BLD_DIR
    	OMPI_DOWNLOAD=$OMPI_URL/v4.0/openmpi-$OPENMPI_VERSION.tar.bz2
    	curl $OMPI_DOWNLOAD | tar -xj
    )


else
   read -p "$BLD_DIR exists. Use it? Otherwise Ctrl+c and remove it." reuse
fi

cd $BLD_DIR/openmpi-$OPENMPI_VERSION

./configure \
    --prefix=/usr/local/openmpi \
    --disable-orterun-prefix-by-default \
    --enable-shared --disable-static \
    --enable-mpi-thread-multiple \
    --enable-mpi-fortran=none \
    --disable-mpi-profile \
    ;

make -j 8 && sudo make install
make distclean
