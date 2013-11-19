#!/usr/bin/env python

from subprocess import Popen,PIPE
import os,sys,string


if not os.getuid() == 0:
    print 'Note: You will obviously only see what you have permission to read.'
    print '-------------------------------------------------------------------'
    print ''


dirs=os.listdir(os.getcwd())
# Du will be reported in kiloBytes
cmnd= ['du', '-sck']+dirs

p = Popen(cmnd,stdout=PIPE,stderr=PIPE)

out,err = p.communicate()

dirs={}
for line in out.split('\n'):
    try:
        du,dir = string.split(line,maxsplit=1)
        dirs[int(du)] = dir
    except:
        continue

for du in sorted(dirs.iterkeys(),reverse=True):
    if du > 1024**2:
        unit = 'G'
        size = du/1024.0**2
    elif du > 1024:
        unit = 'M'
        size = du/1024.0
    else:
        unit = 'K'
        size = du
    print "%7.1f %s %s"%(size,unit, dirs[du])
