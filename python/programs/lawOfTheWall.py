#!/usr/bin/python
#
# uPlus  = 1/k ln(yPlus) + C
# uPlus  = 1/k ln(y*uTao/nu) + C
# uPlus  = 1/k ln(y*(u/uPlus)/nu) + C
# u/uTao = 1/k ln(y*uTao/nu) + C 
# u      = uTao*(1/k ln(y*uTao/nu) + C)
# uTao   = sqrt( taoWall/rho) = sqrt ( du/dy*nu/rho )


import os,sys
from pylab import *

class boundaryLayer:

    def __init__(self,z,nu=1e-6,rho=1.2,z0=0.1,kappa=0.41,Clog=5,Cmu=0.09):
        self.z      = array(z)
        self.nu     = nu
        self.rho    = rho
        self.u      = z
        self.z0     = z0
        self.kappa  = kappa
        self.Cmu    = Cmu
        self.Clog   = Clog

    def taoW(self):
        return self.u[1]/self.z[1]*self.nu

    def uTao(self):
        return sqrt(self.taoW()/self.rho)

    def yPlus(self):
        return self.z*self.uTao()/self.nu

    def uPlus(self):
        return 1./self.kappa*log(self.yPlus())+self.Clog

    def evalU(self):
        lnYplus=array([log(a*self.uTao()/nu) for a in y])
        self.u = self.uTao()*(1./self.kappa*log(self.yPlus()))+self.Clog

    def iterateForU(self,err=1e-6):
        uOld=self.u
        while abs(err)>1e-8:
            self.evalU()
            err=max(uOld-self.u)
            print 'Error = %8f Tao wall = %8f' % (err,self.taoW())
            uOld=self.u


def UHoxey(uPlus,z,z0,kappa=0.41):
    return uPlus/kappa*log(z+z0/z0)

def KHoxey(uPlus,Cmu=0.09):
    return uPlus**2/sqrt(Cmu)

def epsHoxey(uPlus,Cmu=0.09):
    return uPlus**2/sqrt(Cmu)

rho=1.2
nu=1e-5
z0=10
y=array(linspace(1e-5,1000,1000))

BL = boundaryLayer(y,nu=nu,rho=rho)

BL.iterateForU()

plot(BL.z,BL.u)
grid('on')
show()
