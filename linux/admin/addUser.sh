#!/bin/bash

additionalGroups="dialout,cdrom,plugdev,lpadmin,sambashare"
adminGroups="adm,admin"
shell="/bin/bash"

gitToGet="git@endor:/home/nikwik/repositories/git/etc \
          git@endor:/home/nikwik/repositories/git/toolbox"

function ABORT()
{
    echo -e "\n!** $1.\nABORTING!\n"
    exit 1
}

checkIsRoot()
{
    if [ ! $(id -u) = 0 ]; then
        ABORT "You must be root or use sudo to run this script"
    fi
}

function successTest()
{
    if [ $1 != 0 ]; then
        ABORT "Failed: $2"
    fi
}

function checkUserExists()
{
    countUser=$(grep -E -c "^$1:" /etc/passwd)
    countGroup=$(grep -E -c "^$1:" /etc/group)
    if [ ! $countUser = 0 -a ! $countGroup = 0 ]; then
        ABORT "User and/or group already exists. You can use userdel to remove them"
    fi
}

function backup()
{
    SOURCE=$1
    TARGET=$1.bak_$(date +%s)
    echo -e "!** Backup of $SOURCE is $TARGET"
    mv -v $SOURCE $TARGET
}

function addUser()
{
    NAME=$1
    ID=$2

    checkUserExists $NAME

    userHome=/home/$NAME
    if [ -d $userHome ]; then
        echo -ne "*** Folder $userHome already exists! Do you want to remove it?! [y/n]: "
        read confirm
        if [ x$confirm = "xy" -o x$confirm = "xY" ]; then
            backup $userHome
        else
            ABORT  "I do not want to use an exisiting folder for users home."
        fi
    fi

    groupadd -g $ID $NAME
    successTest $? groupadd

    echo -ne "\nShould the new user have admin privileges? [y/n]: "
    read mkadmin
    if [ x$mkadmin = "xy" -o x$mkadmin = "xY" ]; then
        additionalGroups="$additionalGroups,$adminGroups"
    fi

    useradd -u $ID -m -s $shell -g $ID -G $additionalGroups $NAME
    successTest $? useradd

    echo -e "\nSet password for $NAME"

    passwd $NAME
    successTest $? passwd

    echo -e "\nUser $NAME created.\n"
}

checkIsRoot

echo -ne "\nInput new users username: "
read NAME
echo -ne "\nInput new users UID: "
read ID
echo -ne "\nReally create a new user and group with name and id as $NAME and $ID? [y/n]: "
read confirm

if [ x$confirm = "xy" -o x$confirm = "xY" ]; then
    addUser $NAME $ID
else
    ABORT "."
fi

for git in $gitToGet; do
    echo -e "\n*** Attempting to clone git repository $git"
    ( cd /home/$NAME; su $NAME -c "git clone $git" )
done

if [ -f /home/$NAME/etc/sample.bashrc ]; then
    echo -e "\nReplacing /home/$NAME/.bashrc with modified .bashrc"
    rm /home/$NAME/.bashrc
    su $NAME -c "cp -v /home/$NAME/etc/sample.bashrc /home/$NAME/.bashrc"
fi

echo -e "\nEND. Now, go through the files in ~/etc/conf.d to set the software paths right.\n"
