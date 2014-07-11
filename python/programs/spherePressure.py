#!/usr/bin/python
'''Potential flow around a sphere. No gravity'''

from pylab import *

def u(u0,R,r):
    '''
    Velocity distribution along radial vertical
    line from sphere
    '''
    return u0+u0*0.5*(R**3/r**3)

def ptot(u0,p0=0):
    return 0.5*u0**2

def p1(u0,R,r,p0=0):
    '''
    Static pressure from Bernoulli as
    p_0+pDyn_0 = p_1+pDyn_1
    '''
    return ptot(u0,p0)-0.5*(u(u0,R,r))**2

def polyp1(r,coeffs):
    R = zeros(len(r))
    for i,c in enumerate(coeffs[::-1]):
        R += c*r**i
    return R

def waveHeight(p):
    return  p/9.81

R=3.0
u0=2.0
p0=0.
r=linspace(R,6*R,100)

pTot = ptot(u0,p0)

p=array( [p1(u0,R,a) for a in r] )

coeffs = polyfit(r,p,4)
print coeffs

print "p(r/R) r/R = 1", p1(u0,R,1*R)
print "p(r/R) r/R = 2", p1(u0,R,2*R)
print "p(r/R) r/R = 4", p1(u0,R,4*R)
print "p(r/R) r/R = 8", p1(u0,R,8*R)
print "p(r/R) r/R =16 ",p1(u0,R,16*R)
print ''

print "w(r/R) r/R = 1", waveHeight(p1(u0,R,1*R))
print "w(r/R) r/R = 2", waveHeight(p1(u0,R,2*R))
print "w(r/R) r/R = 4", waveHeight(p1(u0,R,4*R))
print "w(r/R) r/R = 6", waveHeight(p1(u0,R,6*R))
print "w(r/R) r/R = 8", waveHeight(p1(u0,R,8*R))

plot(r, p)

#plot(r, -60/r**3)
grid('on')
title('U0={0}, R={1}, p0={2}'.format(u0,R,p0))
xlabel('r')
ylabel('p')


show()
