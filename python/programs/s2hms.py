#!/usr/bin/python

import sys,math

def s2hms(s,sep=':'):
    h = s/3600
    m = (s-h*3600)/60
    s = s-h*3600-m*60
    h,m,s = [ str(i) for i in [h,m,s] ]
    return h+sep+m+sep+s

s=int(sys.argv[1])

print s2hms(s)
