#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,time,random

fmt = '[{{0:{0:s}s}}] {{1:02d}}%'.format(sys.argv[1])
#chars = '-\\|/'
chars = '-oOo'
for i in range(int(sys.argv[1])+1):
    for j in range(10):
        time.sleep(0.5/5)
        sys.stdout.write('\r')
        sys.stdout.write(fmt.format((i-1)*'-'+chars[j%len(chars)],i))
        sys.stdout.flush()
print()


