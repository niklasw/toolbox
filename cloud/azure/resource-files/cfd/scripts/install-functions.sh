#!/usr/bin/env bash

TEST_FILE="empty_file"

function log()
{
    echo -e "$(date +%Y.%m.%d-%T) $@" | tee -a $LOG_FILE
}

function check()
{
    [[ -d "$2" ]] || { log "No MOUNT_PT directory $2"; exit 1; }
    mkdir -p "$3" || { log "Could not create $3"; exit 1; }
    (
        cd "$2"
        curl --silent "$1/empty_file" -O
    )
    log "check() OK"
}

function fetch()
{
    log "fetch() $@"
    resourceUrl="$1"
    fetchFile="$2"    # e.g openfoam/openfoam.sif
    tgtDir="$3"       # e.g. /mnt/linux-pool/software
    DIR="$(dirname $2)"
    FILE="$(basename $2)"
    NAME="${FILE%%.*}"
    
    [[ -d "$tgtDir" ]] || mkdir -p "$tgtDir"

    (
        cd "$tgtDir"
        [[ -d "$DIR" ]] || mkdir -p "$DIR"

        if [ ! -f "$DIR/$FILE" ]
        then
           (cd "$DIR" && curl --silent "$resourceUrl/$fetchFile" -O)
        else
           log "\ttarget already exists for $fetchFile"
        fi
    )
    log "ok"
}

function install_tgz()
{
    # Requires tarball ($fileArg) as /full/path/usr_local_<name>.tgz
    # (or other prefix, but _<name>.tgz must be intact and
    # <name> must also be the name of the top directory in the tgz
    log "install_tgz() $@"
    fileArg="$1"
    installRoot="$2"

    NAME=$(echo $fileArg |sed 's/.*_\(.*\)\.tgz/\1/')

    if [ -n "$installRoot" -a -d "$installRoot" ]
    then
        TAR_ARGS="-C $installRoot"
    else
        log "Could not install $NAME to $installRoot"
        return 1
    fi

    log "Installing $NAME to $installRoot"

    if [ ! -d "$installRoot/$NAME" ]
    then
       tar xfza "$fileArg" $TAR_ARGS
    else
       log "\ttarget already exists for $NAME"
    fi
    log "ok"
}

function install()
{
    log "install() $@"
    # For now, only make symbolic links from /usr/local to
    # software.
    for p in $@
    do
        LINK=/usr/local/$p
        if [ ! -e "$LINK" ]
        then
            ln -sf "$_TGT_DIR/$p" "$LINK"
        fi
    done
    log "ok"
}

function update_rc()
{
    softDir=$1

    log "install update_rc()"
    cat << EOF > /etc/equarc
export PATH=$softDir/singularity/bin:\${PATH}
export MPI_HOME=$softDir/openmpi
export PATH=\$MPI_HOME/bin:\$PATH
EOF
    # Check if /etc/bashrc is already fixed
    if ! $(grep '/etc/equarc' /etc/bashrc > /dev/null 2>&1)
    then
        echo 'source /etc/equarc' >> /etc/bashrc
    fi
    log "ok"
}

function update_user()
{
    U_NAME=$1
    PUB_KEY="$2"
    USER_HOME="$(eval echo ~$U_NAME)"
    SSH_DIR="$USER_HOME/.ssh"
    mkdir -p "$SSH_DIR"
    echo "$PUB_KEY" >>  "$SSH_DIR/authorized_keys"
    chmod 0700 "$SSH_DIR"
    chmod 0600 "$SSH_DIR/authorized_keys"
    chown -R $U_NAME "$SSH_DIR"
}

function configure_blobfuse()
{
    accountName=$1
    accountKey=$2
    containerName=$3
    blobConf=$4
    CONF_DIR="$(dirname $blobConf)"

    if [ ! -d "$CONF_DIR" ]
    then
        mkdir -p "$CONF_DIR"
        chmod 700 "$CONF_DIR"
    fi

    if ! rpm -qa|grep -qe "blobfuse-.*"
    then
        rpm -Uvh https://packages.microsoft.com/config/rhel/7/packages-microsoft-prod.rpm
        yum -y install blobfuse
    fi
    
    cat << EOF > $blobConf
accountName $accountName
accountKey $accountKey
containerName $containerName
EOF
}

function mount_blobfuse()
{
    mountPt=$1
    blobConf=$2
    if ! grep -qs "$mountPt " /proc/mounts
    then
        tmpDir=/mnt/resource/blobfusetmp
        mkdir $mountPt -p
        mkdir $tmpDir -p
        blobfuse $mountPt --tmp-path=$tmpDir \
            --config-file=$blobConf \
            -o attr_timeout=240 \
            -o entry_timeout=240 \
            -o negative_timeout=120 \
            -o allow_other
    fi
}

# Unused
function setup_nfs()
{
    if ! rpm -qa|grep -qe "nfs-utils"
    then
        yum -y install rpcbind nfs-utils
    fi

    NFS_export="$1"
    IP_mask='10.2.0.*'
    cat "$NFS_export ${IP_mask}(rw,noatime)" >> /etc/exports
    systemctl start rpcbind
    systenctl start nfs-server
    exportfs -a
}

# Unused
function setup_ssh_keys()
{
    # Managed by the job creation process
    privateKey="$1"
    network="$2"
    ssh-keygen -t ecdsa -f "$privateKey" -q -N ""
    echo -n 'from="$network" ' >> /etc/ssh/authorized_keys
    cat ${privateKey}.pub >> /etc/ssh/authorized_keys
}
