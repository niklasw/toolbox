#!/usr/bin/env python3 -W ignore
# -*- coding: utf-8 -*-
'''
Example:
Total length L = 4000
Start length dh0 = 25
Max length   dh1 = L/10
Uniform segments nU = 5

after nU uniform segments, increase dh with a*(dh1-dh0)*smoothHeavy

'''

import matplotlib.pyplot as plt
from numpy import *

def molly(x,height,length):
    '''x in [0,1] must return y in [0,1]'''
    y=(tanh((x-1)*pi)+1)*0.5
    return x*length,y*height


L = 32
dh0 = 0.01
dh1 = 10
nU = 5

lU = dh0*nU
lS = L/2-lU

print(lU)

x=linspace(0,1,100)
one = ones(len(x))

xp,yp = molly(x,(dh1-dh0),0.5*(L-2*lU))

X = arange(0,nU)*dh0
X = append(X,xp+lU)
#plt.plot(arange(len(X)),X)

S = arange(0,nU)*dh0

plt.plot(S,ones(len(S)),'-o')

dhBase = arange(len(yp))*dh0

Ss = dhBase + yp + lU

plt.plot(Ss,ones(len(Ss)),'-o')

plt.grid('on')
plt.show()
