#!/usr/bin/python

import re,sys

def getLine(fp,pat):
    line = fp.next()
    while pat.match(line):
        line = getLine(fp,pat)
    return line


afile = sys.argv[1]

fp = open(afile,'r')

pat = re.compile('^\s*$')

print getLine(fp,pat).strip()
print getLine(fp,pat).strip()
