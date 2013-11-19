#!/bin/bash

if [ x$1 = "x" -o x$1 = "x-h" -o x$1 = "x--help" ]; then
    prog=$(basename $0)
    cat << EOF

$prog:
Script to transfer public keys bothways between your machine and a remote host on which
you have an accoount (with the same username). Make sure you have run ssh_keygen -d on
both client and remote host before this script is called.

Note that you will have to enter your password several times before its over.

You need to supply a host name as only argument like this:

$prog hostname

EOF
    
    exit 1
fi
hostname=$1

function tryHost()
{
    ping -c 1 $1 > /dev/null 2>&1
    if [ $? != 0 ]; then
        echo -e "\nHost not reached\n"
        exit 1
    fi
}

function checkLocalFiles()
{
    if [ ! -r $HOME/.ssh/id_dsa.pub ]; then
        echo -e "\nid_dsa.pub not found in $HOME/.ssh"
        echo -e "You may need to run ssh-keygen -d first!\n"
        exit 1
    fi
    echo -e "Local files OK"
}

function checkRemoteFiles()
{
    ssh $1 ls -d $HOME/.ssh        
    if [ $? != 0 ]; then
        echo -e "\nSSH config folder not found on $1\n"
        exit 1
    fi
    ssh $1 ls $HOME/.ssh/id_dsa.pub        
    if [ $? != 0 ]; then
        echo -e "\nid_dsa.pub not found on $1\n"
        echo -e "You may need to run ssh-keygen -d first on $1!\n"
        exit 1
    fi
    echo -e "Remote files OK"
}

tryHost $hostname

checkLocalFiles
checkRemoteFiles $hostname

scp $HOME/.ssh/id_dsa.pub $hostname:.
ssh $hostname 'cat $HOME/id_dsa.pub >> $HOME/.ssh/authorized_keys'
echo -e "\nForward transfer done.\n"
scp $hostname:./.ssh/id_dsa.pub $HOME/.
cat $HOME/id_dsa.pub >> $HOME/.ssh/authorized_keys
echo -e "\nBackward transfer done.\n"
echo -e "\nRemember to remove id_dsa.pub from both home folders.\n"



