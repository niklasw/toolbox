#!/usr/bin/python

import sys
from pylab import *
from waterProperties import WaterProperties

def K2C(K):
    return float(K) - 273.15

def C2K(C):
    return float(C) + 273.15


Fluid = WaterProperties

class solidSurface:
    def __init__(self, T=293.15, emissivity=0.5):
        self.T=T
        self.emissivity=emissivity
        self.sigmaE = 5.6704e-08*self.emissivity

    def radiation(self):
        return self.sigmaE*self.T**4.0

class Solid:
    def __init__(self, T=293.15, conductivity=19, capacity=1000, wall_i=solidSurface(), wall_e=solidSurface()):
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
    def __init__(self, deltaT):
        self.deltaT=deltaT
    def flux(self):
        return 1.28*(self.deltaT) # From openfoam simulation
        #return 0.0*(self.deltaT) # From openfoam simulation

class PipeSection:
    def __init__(self,
                 dx=1.0,
                 D=40e-3,
                 t=2e-3,
                 massFlux=1.0,
                 solid=Solid(),
                 fluid_i=Fluid(),
                 fluid_e=Fluid()):
        self.solid = solid
        self.fluid = fluid_i
        self.ambientFluid  =  fluid_e
        self.length = dx
        self.Di = D
        self.wallThickness = t
        self.Do = self.Di+self.wallThickness*2.0
        self.crossSectionArea = self.Di**2*pi/4

        self.flangeRatio  =  1
        self.innerWallArea = self.length*self.Di*pi
        self.outerWallArea = self.length*self.Do*pi * self.flangeRatio
        self.massFlux = massFlux
        self.U = self.massFlux/self.fluid.density()/self.crossSectionArea
        self.Re = self.Di*self.U/self.fluid.kinematicViscosity()
        self.Pr = 0.7

        self.qi = 0.0
        self.qo = 0.0
        self.Qi = 0.0
        self.Qo = 0.0

        self.Qleak = []
        self.Qclamp = 0.0

        self.leakage = 0.0
        self.deltat = 0.0
        self.roughness = 1e-4

    def update(self, equalWallTemp=False):
        self.Do=self.Di+self.wallThickness*2
        self.crossSectionArea=self.Di**2*pi/4

        self.innerWallArea=self.length*self.Di*pi
        self.outerWallArea=self.length*self.Do*pi * self.flangeRatio
        self.U=self.massFlux/self.fluid.density()/self.crossSectionArea
        self.Re=self.Di*self.U/self.fluid.kinematicViscosity()
        if equalWallTemp:
            self.updateWallTemperature()
            self.updateFluxes(equalWallTemp)
        else:
            self.updateWallTemperatures()
            self.updateFluxes()
        self.fluid.T -= self.deltaT()


    def DittusBoetler(self):
        return 0.023*self.Re**0.8*self.Pr**0.3

    def Hyman(self):
        return 0.53*(self.Pr/(self.Pr+0.952)*self.Grasshof()*self.Pr)**0.25

    def Grasshof(self):
        Ta = self.ambientFluid.T
        Tw = self.solid.outerWall.T
        g = 9.81
        Gr = g * self.ambientFluid.thermalExpansionCoefficient() \
                * (Tw-Ta) * self.Do**3 / self.ambientFluid.kinematicViscosity()**2.0
        return Gr

    def HTCinner(self, setFix=-1.0):
        if setFix < 0:
            return max(self.DittusBoetler()*self.fluid.thermalConductivity()/self.Di,10.0)
        else:
            return setFix

    def HTCouter(self, setFix=-1.0):
        if setFix < 0:
            return self.Hyman()*self.ambientFluid.thermalConductivity()/self.Do
        else:
            return setFix

    def pressureLoss(self, total_length=None):
        import math
        if not total_length:
            total_length = self.length
        r = self.roughness
        d = self.Di
        Re = self.Re
        # Friction factor
        f = 0.25 / (math.log10((r / d) / 3.7 + 5.74 / Re ** 0.9) ** 2)
        # Darcy Weibach
        delta_p = f * (total_length / d) * (self.fluid.density() * self.U ** 2 / 2)
        return delta_p

    def updateWallTemperature(self):
        # Assume constant temp through wall.
        HTCi = self.HTCinner(100)
        HTCe = self.HTCouter(10)
        t = self.wallThickness
        Ti=self.fluid.T-self.deltat/2
        Ta=self.ambientFluid.T

        Tref = self.solid.T
        A = self.solid.outerWall.sigmaE*Tref**4
        B = 4*self.solid.outerWall.sigmaE*Tref**3

        self.solid.T = 1.0/(HTCi+HTCe+B)*(HTCi*Ti+HTCe*Ta-A+B*Tref)
        self.solid.innerWall.T = self.solid.T
        self.solid.outerWall.T = self.solid.T

        # Dumbly iterate
        if abs(self.solid.T - Tref) > 0.0001:
            #sys.stdout.write("*")
            self.updateWallTemperature()

    def updateWallTemperatures(self):
        # Different inside outside wall temp.
        Ai = self.innerWallArea
        Ae = self.outerWallArea
        HTCi = self.HTCinner()
        HTCe = self.HTCouter()
        t = self.wallThickness
        Lambda = self.solid.conductivity
        Ti=self.fluid.T-self.deltat/2
        Ta=self.ambientFluid.T
        Tref = self.solid.outerWall.T

        A = Ae * self.solid.outerWall.sigmaE*Tref**4
        B = Ae * 4*self.solid.outerWall.sigmaE*Tref**3

        g = Lambda/t
        betai=HTCi * Ai
        betae=HTCe * Ae
        G = betai/(g + HTCi)

        Twe = ((betai - HTCi * G) * Ti + betae * Ta + B * Tref - A)/(g * G + betae + B)
        Twi = (Ti * HTCi + Twe * g)/(g + HTCi)

        self.solid.outerWall.T = Twe
        self.solid.innerWall.T = Twi

        if abs(self.solid.outerWall.T - Tref) > 0.0001:
            self.updateWallTemperatures()


    def updateFluxes(self, equalWallTemp=False):
        self.qi = ((self.fluid.T-self.deltat/2)-self.solid.innerWall.T)*self.HTCinner()
        self.qo = (self.solid.outerWall.T-self.ambientFluid.T)*self.HTCouter()
        self.qr = self.solid.outerWall.radiation() / self.flangeRatio
        self.Qo = self.qo*self.outerWallArea
        self.Qr = self.qr*self.outerWallArea
        if equalWallTemp:
            self.Qi = self.qi*self.outerWallArea
        else:
            self.Qi = self.qi*self.innerWallArea
        self.massFlux -= self.leakage
        self.Qleak.append(self.leakage*self.fluid.specificHeat()*(self.fluid.T-self.deltat/2-self.ambientFluid.T))

    def deltaT(self):
        self.deltat = (self.Qclamp+self.Qi)/(self.massFlux*self.fluid.specificHeat())
        return self.deltat


    def info(self):
        str = '\n----------------------------------------------\n'
        str+= '%20s = %6f\n'%('Fluid temperature', self.fluid.T)
        str+= '%20s = %6f\n'%('Fluid temperature2', self.fluid.T-self.deltat/2)
        str+= '%20s = %6f\n'%('Fluid velocity', self.U)
        str+= '%20s = %6f\n'%('Reynolds number', self.Re)
        str+= '%20s = %6f\n'%('Fluid density', self.fluid.density())
        str+= '%20s = %6f\n'%('Inside HTC', self.HTCinner())
        str+= '%20s = %6f\n'%('Outside HTC', self.HTCouter())

        str+= '%20s = %6f\n'%('Inner wall temp', self.solid.innerWall.T)
        str+= '%20s = %6f\n'%('Outer wall temp', self.solid.outerWall.T)

        str+= '----------------------------------------------\n'
        str+= '%20s = %6f\n'%('Inner wall flux', self.Qi)
        str+= '%20s = %6f\n'%('Outer wall flux', self.Qo)
        str+= '%20s = %6f\n'%('Outer wall radiation', self.outerWallArea*self.solid.outerWall.radiation())
        str+= '%20s = %6f\n'%('Flux balance', self.Qi-self.Qo-self.outerWallArea*self.solid.outerWall.radiation())
        str+= '----------------------------------------------\n'
        str+= '%20s = %6f\n'%('Tin-Tout', self.deltaT())
        str+= '----------------------------------------------\n'

        print(str)

def oneD():
    nozzleStartPosition = fullLength-nozzleLength
    nozzleLeakagePerMeter = 0
    dx = fullLength/N
    outerWall=solidSurface(T=T_outerWall, emissivity=Emissivity)
    innerWall=solidSurface(T=T_innerWall)
    steel=Solid(T=T_solid,
                conductivity=solid_conductivity,
                wall_i=innerWall,
                wall_e=outerWall)

    air=Fluid(T=T_flow)
    ambientAir=Fluid(T=T_ambience)

    pipe=PipeSection(\
            dx=dx,\
            D=pipeInnerDiameter, \
            t=pipeWallThickness,\
            massFlux=massFlux,\
            solid=steel,\
            fluid_i=air,\
            fluid_e=ambientAir\
            )

    pipe.flangeRatio = 20

    distance= []
    wallTemperatures = []
    fluxes = {'inner':[],'outer':[],'radiation':[]}
    fluidTemperatures = []

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
        fluidTemperatures.append(pipe.fluid.T)
        fluxes['inner'].append(pipe.Qi)
        fluxes['outer'].append(pipe.Qo)
        fluxes['radiation'].append(pipe.Qr)


    probeLocation = fullLength-0.1
    Tprobe = interp(probeLocation, distance, fluidTemperatures)
    heaterPower =  pipe.massFlux*pipe.fluid.specificHeat()*(T_inlet-Tprobe)

    heatBalance = heaterPower-sum(pipe.Qleak)-clampLoss-sum(fluxes['inner'])

    print("Flowrate                 =  %0.0f [l/m]" % (massFlux*60))
    print("Ambient tank temperature =  %0.1f [C]" %(K2C(T_ambience)))
    print("Temperature at inlet     =  %0.1f [C] "%(K2C(T_inlet)))
    print("Temperature at end probe =  %0.1f [C]" % (K2C(Tprobe)))
    print("Fluxes: outer = %0.1f, inner = %0.1f, radiation = %0.1f"% (sum(fluxes['outer']), sum(fluxes['inner']), sum(fluxes['radiation'])))
    print("HX power = %0.0f" % heaterPower)

    print("Balance: %0.1e W" % (sum(fluxes['inner'])- sum(fluxes['outer'])- sum(fluxes['radiation']),))
    print("Global balance: %0.1e W" % heatBalance)

    #Pressure loss:

    dp = pipe.pressureLoss(fullLength)
    volFlow = massFlux * 3600 / pipe.fluid.density()
    print(f"Pressure loss at flowrate {volFlow:0.1f} m3/h = {dp:0.2g} Pa ({dp/1e4:0.1f} m)")
    print(f"Pipe volume = {0.25 * pipe.Di**2 * pi * fullLength *1e3:0.1f} l")

    if PLOT:
        figure(1, figsize=(7,12), edgecolor='g')
        s=subplot(311)
        title('Fluid temperatures')
        grid()
        text(probeLocation+0.05, Tprobe-273,'Probe\nT = %.0f' % (K2C(Tprobe)), rotation=-90, fontsize=16)
        plot(distance, asarray(fluidTemperatures)-273)
        plot(r_[probeLocation, probeLocation], r_[min(fluidTemperatures), max(fluidTemperatures)]-273,'r--')
        if clampPositions.size:
            text(clampPositions[1], max(fluidTemperatures)-273,'Clamps', rotation=0, fontsize=16)
        for clampPos in clampPositions:
            plot(r_[clampPos, clampPos], r_[min(fluidTemperatures), max(fluidTemperatures)]-273,'g--')
        subplot(312)
        plot(distance, asarray(wallTemperatures)-273)
        title('Outer wall temperatures')
        grid()
        subplot(313)
        plot(distance, asarray(pipe.Qleak)/pipe.length,'r')
        ylabel('W/m')
        title('Nozzle output power')
        text(0.6,10000.,"Total = %.0f W"%sum(pipe.Qleak), rotation=0, fontsize=16)
        grid()
        savefig('pipeHeat.png')
        show()

    return Tprobe

if __name__ == "__main__":
    PLOT = None
    T_ambience = C2K(30)
    T_flow = C2K(35)
    T_inlet = T_flow
    T_solid = 0.5 * (T_ambience + T_flow)
    solid_conductivity = 400
    T_innerWall = T_solid
    T_outerWall = T_solid

    Emissivity = 0.5
    massFlux = 25/60
    pipeInnerDiameter =16e-3
    pipeWallThickness = 1.5e-3

    nozzleLength = 0
    fullLength = 11

    # Assuming 4 clamps, evenly distributed
    clampPositions = array([])
    # Assuming clamp cool end temperature
    clampCoolT = C2K(100)

    N=100

    clampMask=zeros(N)
    nozzleMask = zeros(N)
    pipeSections = linspace(0, fullLength, N)
    oneD()


