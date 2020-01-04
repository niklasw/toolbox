#!/bin/bash
echo "The number of arguments is: $#"
a=${@}
echo "The total length of all arguments is: ${#a}: "
count=0
for var in "$@"
do
    echo "The length of argument '$var' is: ${#var}"
    (( count++ ))
    (( accum += ${#var} ))
done
echo "The counted number of arguments is: $count"
echo "The accumulated length of all arguments is: $accum"


