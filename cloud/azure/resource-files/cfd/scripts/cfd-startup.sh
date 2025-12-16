#!/usr/bin/env bash

# Please avoid whitespaces as in names, folders etc. as far as possible
# since there might be inconsistent quoting in these scripts...
# /niklas

set -e

EXEC_PATH=$(dirname $(realpath $0))

#user equaadmin
_userName=$1
#batch account name rdsa6fz6xcmszyx5q
_accountName=$2
#key apapapa
_accountKey=$3
#poolname linux-pool
_containerName=$4
#the public key needed for $username to access the nodes. Best to be added as
#command line argument, since it's coded into the "pool creation pipeline".
_publicKey="$5"

# Path to generated "LAN" key-paris
#NODES_KEY_PATH=/etc/ssh/ssh_nodes_ecdsa
#NODES_NETWORK="10.2.0.0/16"

#STARTUP_RESOUCES_URL="https://${_accountName}.blob.core.windows.net/scripts"
_RESOURCES_URL="https://equadiststorage.blob.core.windows.net/ice-batch//cfd"
_FUSE_CFG=/etc/blobfuse/fuse_connection.cfg
_MOUNT_PT=/mnt/linux-pool
_TGT_DIR="$_MOUNT_PT/software"
_LOG_FILE="$EXEC_PATH/install.log"
_SOFT_DIR=/usr/local

source $EXEC_PATH/install-functions.sh

log "Started cfd-startup.sh"

update_user "$_userName" "$_publicKey"

configure_blobfuse $_accountName $_accountKey $_containerName $_FUSE_CFG

mount_blobfuse $_MOUNT_PT $_FUSE_CFG

# Install resource software
check $_RESOURCES_URL $_MOUNT_PT $_TGT_DIR

fetch "$_RESOURCES_URL" openfoam/openfoam.sif $_TGT_DIR

for f in openmpi/usr_local_openmpi.tgz singularity/usr_local_singularity.tgz
do
    fetch "$_RESOURCES_URL" $f $_TGT_DIR
    install_tgz $_TGT_DIR/$f $_SOFT_DIR
done

install openfoam
    
update_rc $_SOFT_DIR

#setup_nfs /home/$_userName

#setup_ssh_keys $NODES_KEY_PATH $NODES_NETWORK

log "Finished cfd-startup.sh"
