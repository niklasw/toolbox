#!/usr/bin/env sh

declare -a THE_LIST=( apa banan jungel tarzan )

COUNT_FILE=/dev/shm/apa$PPID #$PPID = pid of parent process

if [[ ! -f $COUNT_FILE || "$1" == "reset" ]]
then
    echo 0 > $COUNT_FILE
fi

function cycle()
{
    listLen=${#THE_LIST[@]}

    declare -i COUNTER=$(cat $COUNT_FILE)

    echo $COUNTER ${THE_LIST[$COUNTER]}

    if (( ++COUNTER < listLen ))
    then
        echo $COUNTER > $COUNT_FILE
    else
        echo 0 > $COUNT_FILE
    fi
}

for i in $(seq 0 9)
do
    cycle
done
