#!/bin/bash

orgBase='/tmp'
newBase=$PWD

for f in VTK/*.vtk; do
    nr=$(echo $f | sed 's/.*_\(.*\)\..*/\1/')
    echo $nr
    sed  -e "s@\(.*_\).*\(\.vtk\)@\1$nr\2@g; s@$orgBase\(/.*\.vtk\)@$newBase\1@g" $1 > ${1%.*}_$nr.pvsm
done

