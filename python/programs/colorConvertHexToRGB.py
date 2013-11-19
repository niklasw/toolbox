#!/usr/bin/python
import sys
hex=sys.argv[1]
hex=hex.lstrip('#')
i=lambda s:int(s,16)
if len(hex) == 6:
    try:
        print 'rgb(%i,%i,%i)'%(i(hex[0:2]),i(hex[2:4]),i(hex[4:6]))
    except:
        print 'Could not convert %s' %hex

