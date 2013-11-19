#!/usr/bin/env python

import os

cwd = os.getcwd()
for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
    dir = dirpath[len(cwd):]
    depth = len(dir)
    print dir+'\n'+' '*(depth)+'/'
    for f in filenames:
        print ' '*(depth-1)+'|_ '+f
