#!/usr/bin/env sh

function az-storage-account-key()
{
    name=${1:-equadiststorage}
    CMD="az storage account keys list --account-name $name -o table"
    AZ_STORAGE_KEY=$($CMD  | awk '$1 ~ "key1" && $2 == "Full" {print $3}')
    export AZ_STORAGE_KEY
}


function az-storage-list-blobs()
{
    [ -n "$AZ_STORAGE_KEY" ] || az-storage-account-key $name
    name=${1:-equadiststorage}
    container=${2:-ice-batch}
    az storage blob list    --container-name $container \
                            --account-name $name \
                            --account-key=$AZ_STORAGE_KEY \
                            -o table
}


echo -e "Azure cli functions defined:\n"
grep -E "function\s*az" ${BASH_SOURCE[0]}
