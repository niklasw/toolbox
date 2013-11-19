#!/usr/bin/env python

import re,sys,os

filein = sys.argv[1]
fileout = sys.argv[2]

print "\nWorking on file:"
print filein
print "\n"

f = open(filein,"r")
lines = f.readlines()
f.close()

pattern = re.compile('\/c[0-9].* { [0-9]\.[0-9].* [0-9]\.[0-9].* [0-9]\.[0-9].* sr} bdef')

newLines = []
gsValue = 0.0
gsInc = 0.5

for line in lines:
    test = pattern.search(line)
    if test:
        print line
        replacement = '{ '+str(gsValue)+' sg }'
        line = re.sub('{.*}',replacement,line)
        print line
        gsValue += gsInc
        gsInc *= 0.5

    newLines.append(line)

f = open(fileout,"w")
for line in newLines:
    f.write(line)
f.close()





