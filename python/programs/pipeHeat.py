#!/usr/bin/python

import sys
from pylab import *

def C2K(C):
    return float(C)+273.15


class Gas:
    def __init__(self,T=293.15,p=1e5,R=287.05):
        self.R=R
        self.T=T
        self.p=p

    def thermalDiffusivity(self):
        return 9.1018E-11*self.T**2 + 8.8197E-08*self.T - 1.0654E-05

    def kinematicViscosity(self):
        return -1.1555E-14*self.T**3 + 9.5728E-11*self.T**2 + 3.7604E-08*self.T - 3.4484E-06

    def thermalConductivity(self):
        return 1.5207E-11*self.T**3 - 4.8574E-08*self.T**2 + 1.0184E-04*self.T - 3.9333E-04

    def densityIdealGasLaw(self):
        p0=1.0e5
        R=287.05
        return p0/R/self.T

    def density(self):
        return 360.77819*self.T**(-1.00336)

    def specificHeat(self):
        return 1.9327E-10*self.T**4 - 7.9999E-07*self.T**3 + 1.1407E-03*self.T**2 - 4.4890E-01*self.T + 1.0575E+03

class solidSurface:
    def __init__(self,T=293.15,emissivity=0.5):
        self.T=T
        self.emissivity=emissivity
        self.sigmaE = 5.6704e-08*self.emissivity

    def radiation(self):
        return self.sigmaE*self.T**4.0

class Solid:
    def __init__(self,T=293.15, conductivity=19, capacity=1000, wall_i=solidSurface(),wall_e=solidSurface()):
        self.T = T
        self.conductivity = conductivity
        self.capacity = capacity
        self.innerWall=wall_i
        self.outerWall=wall_e

    def thermalConductivity(self):
        return self.conductivity

    def heatCapacity(self):
        pass

class Clamp:
    def __init__(self,area=1.0,length=1.0,otherEndTemperature=393,solid=Solid()):
        self.solid=solid
        self.area=area
        self.endTemp=otherEndTemperature
        self.length=length

    def flux(self,T):
        return self.solid.conductivity*(T-self.endTemp)/self.length*self.area


class PipeSection:
    def __init__(self,dx=1.0,D=40e-3,t=2e-3,massFlux=1.0,solid=Solid(),gas_i=Gas(), gas_e=Gas()):
        self.solid=solid
        self.gas=gas_i
        self.ambientGas = gas_e
        self.length=dx
        self.Di=D
        self.wallThickness=t
        self.Do=self.Di+self.wallThickness*2
        self.crossSectionArea=self.Di**2*pi/4

        self.innerWallArea=self.length*self.Di*pi
        self.outerWallArea=self.length*self.Do*pi
        self.massFlux=massFlux
        self.U=self.massFlux/self.gas.density()/self.crossSectionArea
        self.Re=self.Di*self.U/self.gas.kinematicViscosity()
        self.Pr=0.7

        self.qi = 0
        self.qo = 0
        self.Qi = 0
        self.Qo = 0

    def update(self,equalWallTemp=False):
        self.Do=self.Di+self.wallThickness*2
        self.crossSectionArea=self.Di**2*pi/4

        self.innerWallArea=self.length*self.Di*pi
        self.outerWallArea=self.length*self.Do*pi
        self.U=self.massFlux/self.gas.density()/self.crossSectionArea
        self.Re=self.Di*self.U/self.gas.kinematicViscosity()
        if equalWallTemp:
            self.updateWallTemperature()
            self.updateFluxes(equalWallTemp)
        else:
            self.updateWallTemperatures()
            self.updateFluxes()
        self.gas.T -= self.deltaT()


    def DittusBoetler(self):
        return 0.023*self.Re**0.8*self.Pr**0.3

    def Hyman(self):
        return 0.53*(self.Pr/(self.Pr+0.952)*self.Grasshof()*self.Pr)**0.25

    def Grasshof(self):
        Ta=self.ambientGas.T
        Tw=self.solid.outerWall.T
        g=9.81
        Gr=g*1.0/Ta*(Tw-Ta)*self.Do**3/self.ambientGas.kinematicViscosity()**2.0
        return Gr

    def HTCinner(self, setFix=-1.0):
        if setFix < 0:
            return max(self.DittusBoetler()*self.gas.thermalConductivity()/self.Di,10.0)
        else:
            return setFix

    def HTCouter(self,setFix=-1.0):
        if setFix < 0:
            return self.Hyman()*self.ambientGas.thermalConductivity()/self.Do
        else:
            return setFix

    def updateWallTemperature(self):
        # Assume constant temp through wall.
        HTCi = self.HTCinner()
        HTCe = self.HTCouter()
        t = self.wallThickness
        Ti=self.gas.T
        Ta=self.ambientGas.T

        Tref = self.solid.T
        A = self.solid.outerWall.sigmaE*Tref**4
        B = 4*self.solid.outerWall.sigmaE*Tref**3

        self.solid.T = 1.0/(HTCi+HTCe+B)*(HTCi*Ti+HTCe*Ta-A+B*Tref)
        self.solid.innerWall.T = self.solid.T
        self.solid.outerWall.T = self.solid.T

        # Dumbly iterate
        if abs(self.solid.T - Tref) > 0.0001:
            sys.stdout.write("*")
            self.updateWallTemperature()

    def updateWallTemperatures(self):
        # Different inside outside wall temp.
        Ai = self.innerWallArea
        Ae = self.outerWallArea
        HTCi = self.HTCinner()
        HTCe = self.HTCouter()
        t = self.wallThickness
        Lambda = self.solid.conductivity
        Ti=self.gas.T
        Ta=self.ambientGas.T
        Tref = self.solid.outerWall.T

        A = Ae * self.solid.outerWall.sigmaE*Tref**4
        B = Ae * 4*self.solid.outerWall.sigmaE*Tref**3

        g = Lambda/t
        betai=HTCi*Ai
        betae=HTCe*Ae
        G = betai/(g+HTCi)

        Twe = ((betai-HTCi*G)*Ti+betae*Ta+B*Tref-A)/(g*G+betae+B)
        Twi = (Ti*HTCi+Twe*g)/(g+HTCi)

        self.solid.outerWall.T = Twe
        self.solid.innerWall.T = Twi

        if abs(self.solid.outerWall.T - Tref) > 0.0001:
            sys.stdout.write("*")
            self.updateWallTemperatures()


    def updateFluxes(self,equalWallTemp=False):
        self.qi = (self.gas.T-self.solid.innerWall.T)*self.HTCinner()
        self.qo = (self.solid.outerWall.T-self.ambientGas.T)*self.HTCouter()
        self.qr = self.solid.outerWall.radiation()
        self.Qo = self.qo*self.outerWallArea
        self.Qr = self.qr*self.outerWallArea
        if equalWallTemp:
            self.Qi = self.qi*self.outerWallArea
        else:
            self.Qi = self.qi*self.innerWallArea

    def deltaT(self):
        return self.qi*self.innerWallArea/(self.massFlux*self.gas.specificHeat())

    def leakage(self,massFlux):
        self.massFlux -= massFlux

    def info(self):
        str = '\n----------------------------------------------\n'
        str+= '%20s = %6f\n'%('Gas temperature',self.gas.T)
        str+= '%20s = %6f\n'%('Gas velocity',self.U)
        str+= '%20s = %6f\n'%('Reynolds number',self.Re)
        str+= '%20s = %6f\n'%('Gas density',self.gas.density())
        str+= '%20s = %6f\n'%('Inside HTC',self.HTCinner())
        str+= '%20s = %6f\n'%('Outside HTC',self.HTCouter())

        str+= '%20s = %6f\n'%('Inner wall temp',self.solid.innerWall.T)
        str+= '%20s = %6f\n'%('Outer wall temp',self.solid.outerWall.T)

        str+= '----------------------------------------------\n'
        str+= '%20s = %6f\n'%('Inner wall flux',self.Qi)
        str+= '%20s = %6f\n'%('Outer wall flux',self.Qo)
        str+= '%20s = %6f\n'%('Outer wall radiation',self.outerWallArea*self.solid.outerWall.radiation())
        str+= '%20s = %6f\n'%('Flux balance',self.Qi-self.Qo-self.outerWallArea*self.solid.outerWall.radiation())
        str+= '----------------------------------------------\n'
        str+= '%20s = %6f\n'%('Tin-Tout',self.deltaT())
        str+= '----------------------------------------------\n'

        print str

def oneD():
    T_ambience = C2K(50)
    T_flow = C2K(650)
    T_inlet = T_flow
    T_solid = C2K(500)
    solid_conductivity = 19
    T_innerWall = C2K(500)
    T_outerWall = C2K(500)

    massFlux = 0.026
    pipeInnerDiameter = 36e-3
    wallThickness = 2e-3

    nozzleLength = 2*490.0e-3
    fullLength = 298e-3+60e-3+pi*40e-3+nozzleLength
    N=100

    nozzleStartPosition = fullLength-nozzleLength

    nozzleLeakagePerMeter=massFlux/nozzleLength

    dx = fullLength/N

    outerWall=solidSurface(T=T_outerWall, emissivity=0.8)

    innerWall=solidSurface(T=T_innerWall)

    steel=Solid(T=T_solid,conductivity=solid_conductivity,wall_i=innerWall,wall_e=outerWall)

    clamp = Clamp(area=0.02**2,length=0.03,solid=steel)

    air=Gas(T=T_flow)

    ambientAir=Gas(T=T_ambience)

    distance= []
    wallTemperatures = []
    fluxes = {'inner':[],'outer':[],'radiation':[]}
    gasTemperatures = []

    pipe=PipeSection(dx=dx,D=pipeInnerDiameter,t=wallThickness,massFlux=massFlux,solid=steel,gas_i=air,gas_e=ambientAir)

    for i in range(N):
        currentPosition = i*dx
        if currentPosition > nozzleStartPosition:
            pipe.massFlux -= nozzleLeakagePerMeter*pipe.length
            pipe.Di = 40e-3
            pipe.wallThickness = 1.2e-3

        pipe.update()
        pipe.info()

        wallTemperatures.append(pipe.solid.outerWall.T)
        distance.append(currentPosition)
        gasTemperatures.append(pipe.gas.T)
        fluxes['inner'].append(pipe.Qi)
        fluxes['outer'].append(pipe.Qo)
        fluxes['radiation'].append(pipe.Qr)


    print ""
    print "\nAir temperature at inlet = %4f[K], %4f[C] "%(T_inlet,T_inlet-273.15)
    print "\nAir temperature at end =  %4f[K], %4f[C] "%(pipe.gas.T,pipe.gas.T-273.15)
    print "\nFluxes: outer = %f, inner = %f, radiation = %f"% (sum(fluxes['outer']), sum(fluxes['inner']), sum(fluxes['radiation']))
    print "Balance: %e" % (sum(fluxes['inner'])- sum(fluxes['outer'])- sum(fluxes['radiation']),)

    plot(distance,asarray(gasTemperatures)-273)
    show()

if __name__ == "__main__":
    oneD()

