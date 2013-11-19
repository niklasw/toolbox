#!/usr/bin/python
import os

path = os.getcwd()

i = 0
for (path, dirs, files) in os.walk(path):
    print path
    print dirs
    print files
    print "----"
    i += 1
    if i >= 4:
        break

