#!/usr/bin/env python

from pylab import *

x1 = r_[-0.330810,-0.076597]
x2 = r_[-1.961796,0.247827 ]
x3 = r_[-0.482345,1.461979]

s = 0.5*((x2[0] - x3[0])*(x1[0] - x3[0]) - (x2[1] - x3[1])*(x3[1] - x1[1]))
sUnder = (x1[0] - x2[0])*(x3[1] - x1[1]) - (x2[1] - x1[1])*(x1[0] - x3[0])

if sUnder == 0.0:
    print 'Indata error'


s /= sUnder

xc = 0.5*(x1[0] + x2[0]) + s*(x2[1] - x1[1])
yc = 0.5*(x1[1] + x2[1]) + s*(x1[0] - x2[0])

print '\nXc = %f,\nYc = %f\n' % (xc,yc)
