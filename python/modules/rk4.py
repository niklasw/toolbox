#!/usr/bin/python

import os,sys
import pylab
from pylab import pi as PI
from interpolate import interpolatedDataSet

# Fourth order runge kutta for first order ODE
def rk4(f, t,y,dt):
    k1=f(t,y)
    k2=f(t+dt/2, y+dt/2*k1)
    k3=f(t+dt/2, y+dt/2*k2)
    k4=f(t+dt, y+dt*k3)
    return y+dt*(k1+2*k2+2*k3+k4)/6

# Fourth order runge kutta for second order ODE
def rk42(f, t,y,yp,dt,A=0.0,B=0.0):

    k1=dt*f(t,        y,                   yp,        A, B)
    k2=dt*f(t+dt/2.0, y+yp*dt/2,           yp+k1/2.0, A, B)
    k3=dt*f(t+dt/2.0, y+yp*dt/2+k1*dt/4.0, yp+k2/2.0, A, B)
    k4=dt*f(t+dt,     y+yp*dt+k2*dt/2.0,   yp+k3,     A, B)

    yp = yp+1.0/6.0*(k1+2.0*k2+2.0*k3+k4)
    y = y+dt*yp+dt/6*(k1+k2+k3)
    return (y,yp)

def rhs(t,y):
    A=6.0
    B=0.007
    return A*y+B*y**2 

def rprhs(t,y,yp,A,B):
    return 1.0/y*(A-B*yp*yp)

def freeFallRhs(t,y,yp,A,B):
    return A-pylab.sign(yp)*B*yp*yp


if __name__=="__main__":
    def test(y0,t0,t1,dt):
        t=t0
        y=y0
        T=[t0]
        Y=[y0]
        RHS=[rhs(t0,y0)]

        while t<t1:
            t+=dt
            y=rk4(rhs,t,y,dt)
            T.append(t)
            Y.append(y)
    
        print t,y
        pylab.plot(T,Y)
        pylab.grid()
        pylab.show()

    def bubble(r0,t0,t1,dt,dp,rho):
        r0,t0,t1,dt,dp,rho = [ float(a) for a in (r0,t0,t1,dt,dp,rho) ]
        B=3.0/2.0
        Atmp=1.0/rho

        r=r0
        rp=rp0=float(0.0) #Constant volume initially
        t=t0
        T=[t0]
        R=[r0]
        P=[sinus(dp,1,t)]
        while t<t1 and r>0.0:
            pa=sinus(dp,1,t) #Driving ambient pressure
            pb=0.0 # bubble pressure
            A=Atmp*(pa-pb)
            t+=dt
            (r,rp)=rk42(rprhs, t,r,rp,dt,A,B)
            T.append(t)
            R.append(r)
            P.append(pa-pb)

        print "\nDone iterating"

        pylab.subplot(211,title='Bubble radius')
        pylab.plot(T,R,'r')
        pylab.grid()

        pylab.subplot(212,title='Pressure signal')
        pylab.plot(T,P,'b')
        pylab.grid()
        pylab.show()

    def freeFall(h0,v0,t0,t1,dt,g,cd):
        # Test of free fall accelleration with drag a=g-Cd*1/2*rho*u^2
        h0,v0,t0,t1,dt,g,cd = [ float(a) for a in (h0,v0,t0,t1,dt,g,cd) ]
        h=h0
        hp=hp0=float(v0)
        t=float(t0)
        H=[h0]
        T=[t0]
        V=[hp0]
        while t<t1 and pylab.fabs(hp)<101 and h>-0.0001:
            t+=dt
            (h,hp) = rk42(freeFallRhs, t,h,hp,dt,g,cd)
            H.append(h)
            T.append(t)
            V.append(hp)

        pylab.subplot(211,title='Height to Velocity')
        pylab.plot(V,H,'r')
        pylab.grid()

        pylab.subplot(212,title='Velocity')
        pylab.plot(T,V,'b')
        pylab.grid()
        pylab.show()

    def sinus(amp,frq,t):
        return amp*pylab.sin(2*PI*frq*t)

    def constant(value,a,b):
        return float(value)

    def pressureSignal(f, a=0,b=0,c=0):
        return f(a,b,c)

    def runBubble():
        t0=0.0
        t1=1.0
        dt=1.0e-6
        r0=0.001
        dp=2000.0
        rho=1000.0

        bubble(r0,t0,t1,dt,dp,rho)

    def runFreeFall():
        h0=0.0
        v0=10.0
        t0=0.0
        t1=23
        dt=0.01
        g=-9.81
        #sphere
        radius=0.01
        rho=1.2
        areaToVolume=3.0/(radius*4.0)
        cd=0.05
        cdCoeff=0.5*rho*areaToVolume*cd

        freeFall(h0,v0,t0,t1,dt,g,cdCoeff)

    #test(10,0,0.5,0.001)
    #runFreeFall()
    runBubble()


