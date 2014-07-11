#!/usr/bin/python

import glob,sys
import os,shutil
from os.path import join as pjoin

def getEverySecondSorted(items):
    times = []
    floatTimes = []
    for item in files:
        try:
            timeName = os.path.basename(item)
            t = float(timeName)
            floatTimes.append(t)
            times.append(item)
        except:
            print 'Not a time dir: ',item
    ft, nt = (list(t) for t in zip(*sorted(zip(floatTimes, times))))
    rmTimes = [ t for i,t in enumerate(nt) if i%2 != 0 ]
    return rmTimes

procs=glob.glob('processor*')
for p in procs:
    files = glob.glob(pjoin(p,"*"))
    rmTimes = getEverySecondSorted(files)
    print p
    for t in rmTimes:
        print '\t',t
        shutil.rmtree(t)

