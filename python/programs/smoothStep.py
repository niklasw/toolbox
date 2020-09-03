#!/usr/bin/env python3
'''
        a*e^(cr)+b*e^(rx)
f(x) = -------------------
         e^(cr)+e^(rx)

'''
import os,sys
from matplotlib import pyplot as plt
from numpy import exp,array,linespace


def smoothStep(low,high,offset,slope,x):
    a=low
    b=high
    c=offset
    r=slope
    return (a*exp(c*r)+b*exp(r*x))/(exp(c*r)+exp(r*x))

X=linspace(0,10,100)
Y=[]
for x in X:
    Y.append(smoothStep(1,2,4,0.5,x)

plt.plot(X,Y)
plt.grid('on')
plt.show()
    


