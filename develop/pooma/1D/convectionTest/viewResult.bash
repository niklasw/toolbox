#!/bin/bash
file=$1
data=clean$file

cat $file|cut -d = -f 2 > $data

octaveFile="/tmp/plotOctave"

echo "data = load "$data";" > $octaveFile
echo "x=data(1,:);" >> $octaveFile
echo "y=data(2,:);" >> $octaveFile
echo "z=data(3,:);" >> $octaveFile
echo "u=data(4,:);" >> $octaveFile
echo "v=data(5,:);" >> $octaveFile
echo "plot(x,y,x,z,x,u,x,v)" >> $octaveFile
echo "pause(10)" >> $octaveFile

octave $octaveFile
