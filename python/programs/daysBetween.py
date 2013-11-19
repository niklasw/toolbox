#!/usr/bin/python

import dateConverters as DC
import sys

d0=sys.argv[1]
d1=sys.argv[2]
fmt='YYYY-MM-DD:hh-mm-ss'
if len(sys.argv)==4:
    fmt=sys.argv[3]


s0=DC.dateStringToEpoch(d0,fmt)
s1=DC.dateStringToEpoch(d1,fmt)

print 'Days passed =',int((s1-s0)/(3600*24))
