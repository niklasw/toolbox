#!/usr/bin/env bash
# Unused
function setup_ssh_keys()
{
    # Creates ssh key-pair and config for user $3 .ssh folder
    # in given directory ($1) in a temporary location. Then
    # packs these to be easily unpacked in users .ssh dir
    privateKey="$1"
    network="$2"
    userName="$3"
    USER_HOME="$(eval echo ~$userName)"
    USER_CONFIG="$USER_HOME/.ssh/config"

    DIR=$(dirname "$privateKey")
    KEY_NAME=$(basename "$privateKey")
    ssh-keygen -t ecdsa -f "$privateKey" -q -N ""
    [[ -f "$USER_HOME/.ssh/authorized_keys" ]] && \
    	cat "$USER_HOME/.ssh/authorized_keys" > "$DIR/authorized_keys"
    echo -ne "from=\"$network\" " >> "$DIR/authorized_keys"
    cat ${privateKey}.pub >> "$DIR/authorized_keys"
    cat << EOF > "$DIR/config"
 Host ${network%.*}.*
    StrictHostKeyChecking no
    IdentityFile ~/.ssh/$KEY_NAME
EOF
    chown $userName "$USER_CONFIG"

    (
        cd $DIR
        tar czfa /mnt/linux-pool/keys/node_keys.tgz \
                 $KEY_NAME $KEY_NAME.pub authorized_keys config
    )
    rm -f $DIR/{$KEY_NAME,$KEY_NAME.pub,authorized_keys}
}

# Just testing
setup_ssh_keys /dev/shm/node_keys "10.2.0.0/16" equaadmin

