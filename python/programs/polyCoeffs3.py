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

a,b,c,d = polyfit(x,y,3)

print 'Coefficients, highest power first:\n\ta = %f\n\tb = %f\n\tc = %f\n\td = %f' % (a,b,c,d)

print '\nStart exhaust temperature =  %f K' % y[0]
print '\nStart exhaust temperature =  %f C' % (y[0]-273.15)

polynome = '$%0.2e*t^3 + %0.2e*t^2 + %0.2e*t + %0.2e$' % (a,b,c,d)

print '\n\t',polynome

X = linspace(0,1500,1000)

plot(x,y,'r-o',X,a*X**3+b*X**2+c*X+d,'g-')
legend(('data',polynome), loc='lower left')

imagename='polyfit.png'
grid('on')
savefig(imagename)
import subprocess
subprocess.call('eog '+imagename ,shell=True)
