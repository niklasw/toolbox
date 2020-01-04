#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import cumsum,array
import matplotlib.pyplot as plt

def dx(firstDx=0.01,eps=1.15,N=30):
    return [firstDx*eps**i for i in range(N)]

def xCoord(firstDx=0.01,eps=1.15,N=30):
    return cumsum(dx(firstDx,eps,N))

X = xCoord(0.02,1.33,32)
print(X)
