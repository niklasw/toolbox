#!/usr/bin/python

import numpy,sys

def interactor(astring):
    import sys
    print astring
    return sys.stdin.readline().strip()


def shift(u, offset):
      offset %= len(u)
      return numpy.concatenate((u[-offset:], u[:-offset]))

def Heaviside(u,s=0):
    gt=lambda a: int(a>s)
    return numpy.asarray(map(gt,u))

def dx(u,h,s=0): #first derivatives
    rh=1.0/h
    if s==0: # central difference
        ux = 0.5*rh*(shift(u,-1)-shift(u,1))
        return ux
    elif s==-1: # backward
        ux = rh*(u-shift(u,-s))
        ux[0]=ux[-1]
        return ux
    elif s==1: # forward
        ux= rh*(shift(u,-s)-u)
        ux[-1]=ux[0]
        return ux
    else:
        return numpy.zeros(u.size)

def dxx(u,h): # second order second derivative, 'central'
    return 1.0/h*(dx(u,h,1)-dx(u,h,-1))

def eno2(u,h): # second order eno
    ux=dx(u,h,-1)
    uxx=dxx(u,h)
    mask=Heaviside(abs(shift(uxx,1))-abs(uxx))
    uxx=(1-mask)*shift(uxx,1)+mask*uxx
    return ux+uxx*h*0.5

# ------------------------------------------------------------------------
# Some functions to test the operators

def diffTest(f,N):
    from numpy import pi
    import pylab
    X=numpy.linspace(-1.0,1.0,N)
    h=2.0/(N-1)
    u0=f(2*pi*X)

    pylab.plot( X,u0,'r-x', X,eno2(u0,h),'k-o',X,dx(u0,h),'r-o', X,dx(u0,h,1),'g-o',X,dx(u0,h,-1),'b-o')
    pylab.show()

    # interactor('Press enter to continue')
    return

def convectionTest(f,N,CFL,t1=1):
    print """
        Plotting does not work. Don\'t know why it doesnt update the plot.
        """
    from numpy import pi
    import pylab
    t0=0.0

    X=numpy.linspace(-1.0,1.0,N)
    h=2.0/(N-1)
    u0=f(pi*X)
    u0[N-1]=u0[0]
    dt=CFL*h
    T=dt
    u=u0
    uOld=u0
    uOldOld=uOld

    # plot
    plotInterval=4
    pylab.title('CLOSE THIS WIDOW TO START (press the x button top right)')
    pylab.show()
    pylab.title('Plotting every '+str(plotInterval)+' iteration. CFL = '+str(CFL))
    pylab.plot(X,u0,'g-s')
    pylab.draw()
    pylab.grid()
    line,=pylab.plot(X,u,'r-o')
    pylab.axis([-1,1,-.5,1.5])

    iter=0
    while T<=t1:
        iter+=1

        ux=dx(uOld,h,-1)
        #ux=eno2(uOld,h)
        u=uOld-dt*ux
        uOld=u
        uOldOld=uOld

        #update plot. Is a bit slow plottin, so reducing exec time by this.
        if not iter % plotInterval:
            line.set_ydata(u)
            pylab.draw()

        T+=dt
        print T
    line.set_ydata(u)
    pylab.draw()
    
    interactor('Press enter to continue')

# ------------------------------------------------------------------------
# main program. Called if this file is 'main'
# All defined functions can be made accessible from other programs
# by "from myOperators import *" Then everything, EXCEPT the following 
# if-statement is imported.

if __name__=='__main__':
    import numpy
    if len(sys.argv)!=0:
        g=lambda x:numpy.cos(x)
        diffTest(g,64)
        sys.exit(0)
    else:
        g=lambda x: Heaviside(numpy.cos(x))
        convectionTest(g,32,0.6,2)

