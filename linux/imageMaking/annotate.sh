#!/bin/bash
#
# Annotate a numbered sequence of images with timestamps

let count=0
for Time in $(seq 30 30 28000)
do
    filename=$(printf temperature_1.%04d.png $count)
    (( count ++ ))

    if [ -f "$filename" ]
    then
        ANNOTATION=$(printf "Time: %05d s" $Time)
        magick $filename -gravity "NorthWest" -pointsize 24 -annotate +20+10 "$ANNOTATION" t_$filename
        echo $filename
    fi
done
