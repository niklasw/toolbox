#!/usr/bin/env sh

function lookup_config()
{
    while read line
    do
        var=$(awk '{print $1}' <<< $line)
        if [[ "$var" == "$2" ]]
        then
            val=$(awk '{print $2}' <<< $line)
            echo $val
            return 0
        fi
    done < $1
    echo "${1}_not_found"
    return 1
}

batch_account=$(lookup_config $1 batch_account)
echo $batch_account
