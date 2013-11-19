#!/usr/bin/python

import sys,os,pylab,matplotlib

def reverse(a):
    b=[]
    for i in range(len(a)):
        j=len(a)-i-1
        b.append(a[j])
    return b

args = [ float(a) for a in sys.argv[1:5] ]
m,n,a,b=args

x=pylab.linspace(0,a,1000)

y=b*pow((1-pow((x/a),m)),(1/n))

x0=reverse(-x)
X=pylab.concatenate((x0,x))

y0=reverse(y)
Y=pylab.concatenate((y0,y))

matplotlib.axis = [-a,a,-b,b]
pylab.plot(X,Y)

pylab.show()


