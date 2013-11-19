#!/usr/bin/env python

import re,sys,os,string,fileinput

fhout=open(sys.argv[1]+'.clean','w')

for line in fileinput.input():
     if re.search(r'=',line):
          line=line.split('=')[1]
          fhout.write(line)

fhout.close()

os.popen("octave octaveInput")

