#!/usr/bin/env python

import sys,fileinput

args=sys.argv

if len(sys.argv)!=3:
    print "Usage: ", args[0], "<infile> <N>"
    print "Output is sent to stdout"
    sys.exit(0);

file=args[1]
N=int(args[2])

i=0
for line in fileinput.input(file):
    i+=1
    line=line[:-1]
    if (i%N) == 0:
        print line

