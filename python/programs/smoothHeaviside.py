#!/usr/bin/python

from numpy import array,arange,linspace
import matplotlib.pyplot as plt


def smoothStep(s0,s1,x):
    out = 1.0
    if (s1-s0)>1e-12:
        x = min(max(x,s0),s1)
        x = (x - s0)/(s1 - s0);
        out = pow(x,3)*(x*(x*6 - 15) + 10);
    return out

x=linspace(0,1,500)

s0=0.5
s1=0.8
H = array([smoothStep(s0,s1,a) for a in x])
print(H.shape)
print(x.shape)
plt.plot(x,(H))
plt.grid()
plt.show()

