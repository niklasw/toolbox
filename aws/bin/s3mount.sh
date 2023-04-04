#!/usr/bin/env bash

function ensure_dir()
{
    if [ ! -d "$1" ]
    then
        read -p "$1 does not exist. Create it or Ctrl-C" 
        sudo mkdir -p "$1"
        sudo chown $USER $1
    fi
}

declare -a S3_BUCKETS
S3_BUCKETS[0]="nikwik-backup"
S3_BUCKETS[1]="nikwik-photos"
S3_BUCKETS[2]="nikwik-base-bucket"

MNT_ROOT=/mnt/s3

function mount_()
{
    for B in ${S3_BUCKETS[*]}
    do
        MNT_PT="$MNT_ROOT/$B"
        ensure_dir "$MNT_PT"
        if mountpoint -q $MNT_PT
        then
            echo "$MNT_PT is already a mountpoint"
        else
            s3fs $B $MNT_PT -o uid=1000
            [[ $? == 0 ]] && echo "Mounted $B" || echo "Mount $B failed"
        fi
    done
}

function umount_()
{
    for B in ${S3_BUCKETS[*]}
    do
        MNT_PT="$MNT_ROOT/$B"
        umount "$MNT_PT"
    done
}

if [[ "$1" == -u ]]
then
    umount_
else
    mount_
fi
