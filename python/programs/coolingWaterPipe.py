#!/usr/bin/python

import sys
from pylab import *

def C2K(C):
    return float(C)+273.15

def K2C(K):
    if (float(K)-273.15) < 0:
        print 'Temperature error in K2C'
        sys.exit(1)
    return float(K)-273.15

# waterProperties work with Celsius!
from waterCalc import waterProperties

class Water:
    # @25 C mostly...

    def __init__(self,T=293.15,p=1e5,R=287.05):
        self.R=R
        self.T=T
        self.TC = K2C(T)
        self.p=p
        self.properties = waterProperties()

    def thermalDiffusivity(self):
        return 0.143e-6

    def kinematicViscosity(self):
        self.properties.selectProperty('nu')
        return self.properties.getPropertyValue(self.TC)

    def thermalConductivity(self):
        return 0.58

    def density(self):
        self.properties.selectProperty('rho')
        return self.properties.getPropertyValue(self.TC)

    def specificHeat(self):
        self.properties.selectProperty('Cp')
        return self.properties.getPropertyValue(self.TC)*1e3

    def Prandtl(self):
        self.properties.selectProperty('Pr')
        #print self.properties.getPropertyValue(self.TC)
        return self.properties.getPropertyValue(self.TC)


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
    def __init__(self,T=293.15,emissivity=0.0):
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

class PipeSection:
    def __init__(self,dx=1.0,D=10-3,t=10e-3,massFlux=1.0,solid=Solid(),gas_i=Water(), gas_e=Gas(), shieldRadius=0):
        self.solid=solid
        self.gas=gas_i
        self.ambientGas = gas_e
        self.length=dx
        self.Di=D
        self.wallThickness=t
        self.Do=self.Di+self.wallThickness*2.0
        self.shieldRadius = shieldRadius
        self.shieldFactor = 0.5*self.shieldRadius/(self.Do/2.0)
        if not self.shieldRadius:
            print "SHIELDS DOWN"
            self.shieldFactor = 1.0
        self.crossSectionArea=self.Di**2*pi/4

        self.innerWallArea=self.length*self.Di*pi
        self.outerWallArea=self.length*self.Do*pi
        self.massFlux=massFlux
        self.U=self.massFlux/self.gas.density()/self.crossSectionArea
        self.Re=self.Di*self.U/self.gas.kinematicViscosity()

        self.qi = 0.0
        self.qo = 0.0
        self.Qi = 0.0
        self.Qo = 0.0

        self.Qleak = []
        self.Qclamp = 0.0

        self.leakage = 0.0
        self.deltat = 0.0
        print self.massFlux

    def update(self):
        self.Do=self.Di+self.wallThickness*2
        self.crossSectionArea=self.Di**2*pi/4

        self.innerWallArea=self.length*self.Di*pi
        self.outerWallArea=self.length*self.Do*pi
        self.U=self.massFlux/self.gas.density()/self.crossSectionArea
        self.Re=self.Di*self.U/self.gas.kinematicViscosity()
        self.updateWallTemperatures()
        self.updateFluxes()
        self.gas.T -= self.deltaT()


    def DittusBoetler(self):
        return 0.023*self.Re**0.8*self.gas.Prandtl()**0.3

    def Hyman(self):
        print "HYMAN",0.53*(self.gas.Prandtl()/(self.gas.Prandtl()+0.952)*self.Grasshof()*self.gas.Prandtl())
        return 0.53*(self.gas.Prandtl()/(self.gas.Prandtl()+0.952)*self.Grasshof()*self.gas.Prandtl())**0.25

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

    def updateWallTemperatures(self):
        # Different inside outside wall temp.
        Ai = self.innerWallArea
        Ae = self.outerWallArea
        HTCi = self.HTCinner()
        HTCe = self.HTCouter()
        t = self.wallThickness
        Lambda = self.solid.conductivity
        Ti=self.gas.T-self.deltat/2
        Ta=self.ambientGas.T
        Tref = self.solid.outerWall.T

        A = Ae * self.solid.outerWall.sigmaE*Tref**4
        B = Ae * 4*self.solid.outerWall.sigmaE*Tref**3

        A*= self.shieldFactor
        B*= self.shieldFactor

        g = Lambda/t
        betai=HTCi*Ai
        betae=HTCe*Ae
        G = betai/(g+HTCi)

        Twe = ((betai-HTCi*G)*Ti+betae*Ta+B*Tref-A)/(g*G+betae+B)
        Twi = (Ti*HTCi+Twe*g)/(g+HTCi)

        self.solid.outerWall.T = Twe
        self.solid.innerWall.T = Twi
        print Twi, Twe

        if abs(self.solid.outerWall.T - Tref) > 0.0001:
            self.updateWallTemperatures()


    def updateFluxes(self):
        self.qi = ((self.gas.T-self.deltat/2)-self.solid.innerWall.T)*self.HTCinner()
        self.qo = (self.solid.outerWall.T-self.ambientGas.T)*self.HTCouter()
        self.qr = self.solid.outerWall.radiation()*self.shieldFactor
        self.Qo = self.qo*self.outerWallArea
        self.Qr = self.qr*self.outerWallArea
        self.Qi = self.qi*self.innerWallArea
        self.massFlux -= self.leakage
        self.Qleak.append(self.leakage*self.gas.specificHeat()*(self.gas.T-self.deltat/2-self.ambientGas.T))

    def deltaT(self):
        self.deltat = (self.Qclamp+self.Qi)/(self.massFlux*self.gas.specificHeat())
        return self.deltat


    def info(self):
        str = '\n----------------------------------------------\n'
        str+= '%20s = %6f\n'%('Gas temperature',self.gas.T)
        str+= '%20s = %6f\n'%('Gas temperature2',self.gas.T-self.deltat/2)
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
    nozzleStartPosition = fullLength-nozzleLength
    nozzleLeakagePerMeter=massFlux/nozzleLength
    dx = fullLength/N
    outerWall=solidSurface(T=T_outerWall, emissivity=0.0)
    innerWall=solidSurface(T=T_innerWall)
    steel=Solid(T=T_solid,conductivity=solid_conductivity,wall_i=innerWall,wall_e=outerWall)

    water=Water(T=T_flow)
    ambientAir=Gas(T=T_ambience)

    pipe=PipeSection(\
            dx=dx,\
            D=pipeInnerDiameter, \
            t=pipeWallThickness,\
            massFlux=massFlux,\
            solid=steel,\
            gas_i=water,\
            shieldRadius = shieldRadius,\
            gas_e=ambientAir\
            )

    distance= []
    wallTemperatures = []
    fluxes = {'inner':[],'outer':[],'radiation':[]}
    gasTemperatures = []

    clampLoss = 0.0

    for i in range(N):
        currentPosition = i*dx
        pipe.leakage = 0.0
        pipe.Di = pipeInnerDiameter
        pipe.wallThickness = pipeWallThickness

        pipe.update()
        pipe.info()

        wallTemperatures.append(pipe.solid.outerWall.T)
        distance.append(currentPosition)
        gasTemperatures.append(pipe.gas.T)
        fluxes['inner'].append(pipe.Qi)
        fluxes['outer'].append(pipe.Qo)
        fluxes['radiation'].append(pipe.Qr)


    probeLocation = fullLength-0.1
    Tprobe = interp(probeLocation,distance,gasTemperatures)
    heaterPower =  massFlux*pipe.gas.specificHeat()*(T_inlet-T_ambience)

    print "Air temperature at inlet = %4f[K], %4f[C] "%(T_inlet,T_inlet-273.15)
    print "Air temperature at end probe = %4f[K], %4f[C]" % (Tprobe,Tprobe-273.15)
    print "Fluxes: outer = %f, inner = %f, radiation = %f"% (sum(fluxes['outer']), sum(fluxes['inner']), sum(fluxes['radiation']))
    print "Total clamp loss = %f" % clampLoss
    print "Heater input power = %f" % heaterPower

    print "Nozzle output total flux = %f" % sum(pipe.Qleak)
    print "Balance: %e" % (sum(fluxes['inner'])- sum(fluxes['outer'])- sum(fluxes['radiation']),)

    print "Global balance: %e" % (heaterPower-sum(pipe.Qleak)-clampLoss-sum(fluxes['inner']),)

    figure(1,figsize=(7,12),edgecolor='g')
    s=subplot(311)
    title('Gas temperatures')
    grid()
    text(probeLocation+0.05,Tprobe-273,'Probe\nT = %.0f' % (Tprobe-273.15),rotation=-90,fontsize=16)
    plot(distance,asarray(gasTemperatures)-273)
    plot(r_[probeLocation,probeLocation],r_[min(gasTemperatures),max(gasTemperatures)]-273,'r--')
    if clampPositions.size:
        text(clampPositions[1],max(gasTemperatures)-273,'Clamps',rotation=0,fontsize=16)
    for clampPos in clampPositions:
        plot(r_[clampPos,clampPos],r_[min(gasTemperatures),max(gasTemperatures)]-273,'g--')
    subplot(312)
    plot(distance,asarray(wallTemperatures)-273)
    title('Outer wall temperatures')
    grid()
    subplot(313)
    plot(distance,asarray(pipe.Qleak)/pipe.length,'r')
    ylabel('W/m')
    title('Nozzle output power')
    text(0.6,10000.,"Total = %.0f W"%sum(pipe.Qleak),rotation=0,fontsize=16)
    grid()
    savefig('pipeHeat.png')
    show()

if __name__ == "__main__":

    T_ambience = C2K(50)
    T_flow = C2K(20)
    T_inlet = T_flow
    T_solid = C2K(20)
    solid_conductivity = 400.0
    T_innerWall = C2K(20)
    T_outerWall = C2K(20)

    massFlux = 0.1 
    pipeInnerDiameter = 36e-3
    pipeWallThickness = 2e-3

    nozzleWallThickness = 1.2e-3
    nozzleInnerDiameter = 40e-3

    shieldRadius = 0.0 #nozzleInnerDiameter/2.0+nozzleWallThickness+shieldDistance

    nozzleLength = 2*490.0e-3
    fullLength = 298e-3+60e-3+pi*40e-3+nozzleLength

    # Assuming 4 clamps, evenly distributed
    clampPositions = fullLength - nozzleLength*r_[4,3,2,1]/5.0
    #clampPositions = array([])
    # Assuming clamp cool end temperature
    clampCoolT = C2K(100)

    N=10

    pipeSections = linspace(0,fullLength,N)
    oneD()

