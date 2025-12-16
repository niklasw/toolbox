#!/usr/bin/env sh

function az-storage-account-key()
{
    # Needs to login with niklas.wikstom@equa.se
    name=${1:-equadiststorage}
    CMD="az storage account keys list --account-name $name -o table"
    AZ_STORAGE_KEY=$($CMD  | awk '$1 ~ "key1" && $2 == "Full" {print $3}')
    export AZ_STORAGE_ACCOUNT=equadiststorage
    export AZ_STORAGE_CONTAINER=ice-batch
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


function az-storage-downoad()
{
    [ -n "$AZ_STORAGE_KEY" ] || az-storage-account-key $name
    source_path=${1:-cfd}
    target_path=${2:-/tmp}
    az storage blob directory download --container $AZ_STORAGE_CONTAINER \
                                       --account-name $AZ_STORAGE_ACCOUNT \
                                       --account-key $AZ_STORAGE_KEY \
                                       --source-path "$source_path" \
                                       --destination-path "$target_path"\
                                       --recursive

                                        
    
}


echo -e "Azure cli functions defined:\n"
grep -E "function\s*az" ${BASH_SOURCE[0]}
