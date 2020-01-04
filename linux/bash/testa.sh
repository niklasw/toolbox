#!/bin/bash

if [ $# -gt 1 ]; then
    echo ${@:1:${#}-1}
fi
echo ${!#}
echo $#

echo ---------

PARALLEL=false
MESH=false
RUN=false
NP=1
for i in $@ ; do
    opt=$1
    case $opt in
        "-run")
            RUN=true
            shift 1
            ;;
        "-mesh")
            MESH=true
            shift 1
            ;;
        "-np")
            NP=$2
            PARALLEL=true
            shift 2
            ;;
        "*")
            echo $opt
            break 
            ;;
    esac
done


if $PARALLEL; then
    echo Parallel
else
    echo Serial
fi

if $MESH; then
    echo Mesh
fi

if $RUN; then
    echo Run
fi

