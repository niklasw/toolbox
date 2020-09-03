#!/usr/bin/env python

import sys
from airProperties import AirProperties

temperatures = sys.argv[1:]
tList=[]
for s in temperatures:
    try:
        tList.append(float(s))
    except:
        print("\nCould not read input: ",s)

for t in tList:
    air = AirProperties(T=t)
    print(air)

