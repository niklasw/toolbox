#!/usr/bin/env python

from numpy import *

from airProperties import AirProperties
from interactor2 import interactor


class Flow:
    def __init__(self,Q=0.1,media=AirProperties()):
        self.media=media
        self.Q=Q

class Pipe:
    def __init__(self,length=1.0,diameter=0.1,rough=0.05e-3):
        self.length=float(length)
        self.diameter=float(diameter)
        self.rough = rough
        self.area = pi*self.diameter**2/4


class pipeFlow:
    def __init__(self,pipe=Pipe(),flow=Flow()):
        self.pipe=pipe
        self.flow=flow
        self.turbulent = ( self.Re() > 4000 )

    def Re(self):
        return self.pipe.diameter*self.flow.Q/(self.pipe.area*self.flow.media.kinematicViscosity())

    def frictionFactor(self):
        if self.turbulent:
            ff =  (
                    1.14-2*log10(self.pipe.rough/self.pipe.diameter + 21.25
                    / (self.Re()**0.9))
                  )**(-2)
        else:
            ff = 64.0/self.Re()
        return ff

    def pressureLoss(self):
        rho = self.flow.media.densityIdealGasLaw()
        U = self.flow.Q/self.pipe.area
        f = self.frictionFactor()
        return 0.5*rho*U**2*f*self.pipe.length/self.pipe.diameter


if __name__=='__main__':

    L   = 10
    D   = 5e-2
    Q   = 0.057
    r   = 0.01 # [mm]

    i = interactor()

    L = i.get('Pipe length (m) ',test=float,default=L)
    D = i.get('Pipe diameter (m) ',test=float,default=D)
    Q = i.get('Volume flux (m^3/s) ',test=float,default=Q)
    r = i.get('Wall roughness (mm) ',test=float,default=r)/1e3

    T = i.get('Temperature (C) ',test=float,default=20)+273.15
    P = i.get('Reference p (Pa) ',test=float,default=1e5)

    air = AirProperties(T=T,p=P)

    flow = Flow(Q=Q,media=air)
    pipe = Pipe(length=L,diameter=D,rough=r)

    p = pipeFlow(pipe,flow)

    print ''
    i.info('* '*20)
    i.info('Re            = %0.1e' % (p.Re()) )
    i.info('Pressure loss = %0.2e Pa' % (p.pressureLoss()) )
    i.info('* '*20)
    print

