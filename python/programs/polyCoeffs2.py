#!/usr/bin/env python

import sys
from pylab import *
import numpy

try:
    data = numpy.loadtxt(sys.argv[1],skiprows=1)
except:
    try:
        data = numpy.loadtxt(sys.argv[1],skiprows=1,delimiter=',')
    except:
        print "Cannot load data file: should be supplied as first argument. First row is comment."
        sys.exit(1)

x = array(data[:,0])
y = array(data[:,1])+273.15
x -= x[0]

a,b,c = polyfit(x,y,2)

print 'Coefficients, highest power first:\n\ta = %f\n\tb = %f\n\tc = %f' % (a,b,c)

print '\nStart exhaust temperature =  %f K' % y[0]
print '\nStart exhaust temperature =  %f C' % (y[0]-273.15)

polynome = '%0.2e*t^2 + %0.2e*t + %0.2e' % (a,b,c)

print '\n\t',polynome

plot(x,y,'r-o',x,a*x**2+b*x+c,'g-')
legend(('data',polynome))

imagename='polyfit.png'
grid('on')
savefig(imagename)
import subprocess
subprocess.call('eog '+imagename ,shell=True)
