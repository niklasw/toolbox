#!/usr/bin/python

from pylab import *
import sys,os

p0=float(sys.argv[1])
p1=float(sys.argv[2])

p=linspace(p0,p1,200)

Tb=100.+.0002772*(p-101000.)-1.24e-9*(p-101000.)**2
plot(p,Tb)
grid()
show()

