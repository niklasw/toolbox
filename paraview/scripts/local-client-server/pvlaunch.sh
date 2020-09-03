#!/usr/bin/bash --login

PV_HOME=/home/software/ParaView/client-git
MPIRUN=/usr/lib64/openmpi/bin/mpirun
PVSERVER=$PV_HOME/bin/pvserver
PARAVIEW=$PV_HOME/bin/paraview

NP=${1:-16}
SP=${2:-22222}
FROM_PVSC=${3:-no}

NVINDEX_LIB=/home/software/ParaView/nvindex/lib

LOG=/tmp/pvlaunch.log

trap "sleep 2; pkill -9 pvserver" INT TERM EXIT HUP

export LD_LIBRARY_PATH=$NVINDEX_LIB

if [[ $FROM_PVSC == yes ]]
then
    ssh -X localhost "LD_LIBRARY_PATH=$NVINDEX_LIB $MPIRUN --np $NP \
        $PVSERVER --server-port=$SP"
else
    $PARAVIEW --server-url=cs://localhost:$SP > $LOG 2>&1 &
    $MPIRUN --np $NP $PVSERVER --server-port=$SP
fi

