#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def splitp(path,n):
    d=path
    tail=[]
    for i in range(n):
        d,r=os.path.split(d)
        tail.append(r)
        if len(d) == 1:
            break
    tail = tail[::-1]
    return os.path.join(*tail)


P=os.getenv('PYTHONPATH')

print P
print splitp(P,2)
print splitp(P,3)
print splitp(P,4)
print splitp(P,12)



