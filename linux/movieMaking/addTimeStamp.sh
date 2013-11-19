#!/bin/bash

fileName=$1
temp=${1#*e0}
time=${temp%.*}

convert $1  -fill white  -undercolor '#00000080' \
        -font Helvetica \
        -pointsize 40\
        -gravity SouthWest \
        -annotate +10+10 "Time = $time s" ${1%.*}_stamped.png


