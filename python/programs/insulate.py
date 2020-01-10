#!/usr/bin/python

from numpy import array,cos,pi
import sys, os

def Error(s):
    print(s)
    sys.exit(1)

class House:
    '''This is silly, really.
    Make proper config container or somethign FIXME'''
    L = 11.47
    W = 7.68
    hFront = 5.885 #6.485-0.6
    hBack = 3.150 #3750-0.6
    tWall = 0.40
    hTop = 8.6
    nOldWindows=15
    nNewWindows=2
    windowArea=1.82
    lift = 0.6

    roofAngle = 35

    windowsU = 0.7

    @staticmethod
    def oldWallsArea():
        A = House.L*(House.hFront+House.hBack-2*House.lift)
        A+= House.W*(House.hFront-House.lift)*2
        A-= House.nOldWindows*House.windowArea
        return A
    @staticmethod
    def newWallsArea():
        A = (House.L+House.W)*House.lift*2 + House.W*(House.hTop-House.hFront)
        A-= House.nNewWindows*House.windowArea
        return A
    @staticmethod
    def totalWallArea():
        return House.oldWallsArea()+House.newWallsArea()
    @staticmethod
    def totalWindowArea():
        return (House.nOldWindows+House.nNewWindows)*House.windowArea
    @staticmethod
    def roofArea():
        return House.L*House.W/cos(35*pi/180)

    @staticmethod
    def totalHouseArea():
        return House.totalWallArea()+House.roofArea()+House.totalWindowArea()

    @staticmethod
    def volume():
        return 75.0*3*2.4


class material:
    def __init__(self,Lambda=0.14):
        self.L = Lambda         # W/mK

    def __str__(self):
        return 'Material lambda = {0}'.format(self.L)

    def U(self,t):
        return self.L/t    # W/m2K

    def R(self,t):
        return 1/self.U(t)       # m2K/W

    def clone(self):
        return material(self.L)

class component:
    def __init__(self,material, width=0.045):
        self.material = material
        self.width = width

    def sA(self,cc): # specific area
        return self.width/cc

    def AU(self,cc,t):            # W/K
        return self.material.U(t)*self.sA(cc)

    def clone(self):
        return component(self.material.clone(),self.width)

class layer:
    def __init__(self, thickness=1.0, cc=0.6, components=[],insulation=True):
        self.components = components
        self.t = thickness
        self.cc = cc
        self.insulation=insulation

    def __str__(self):
        s = 'Layer:\n'
        s+= 'thickness = {0}\n'.format(self.t)
        #s+= 'CC        = {0}\n'.format(self.cc)
        for c in self.components:
            s+= c.material.__str__()+'\n'
        return s

    def addComponent(self, component):
        self.components.append(component)

    def Assert(self):
        sA = sum([c.sA(self.cc) for c in self.components])
        if abs(sA-1.0) > 1e-6:
            for c in self.components:
                print(c.sA(self.cc))
            Error('Layer coverage error: sA = {0}'.format(sA))

    def U(self):
        self.Assert()
        if self.insulation:
            return sum([c.AU(self.cc,self.t) for c in self.components])
        else:
            return 1e9

    def R(self):
        return 1/self.U()

    def clone(self,thickness):
        newLayer = layer(thickness,self.cc)
        for c in self.components:
            newLayer.addComponent(c.clone())
        return newLayer

class buildingSurface(list):
    def __init__(self,layers=[],name='Wall',element='wall'):
        list.__init__(layers)
        self.name=name
        self.area = 1.0
        self.element=element
        self.Rsi = {'wall':0.13,'roof':0.10}
        self.Rse = {'wall':0.13,'roof':0.04} # Assuming luftspalt in walls
        print('Building {0}'.format(name))

    def U(self):
        Rsi = self.Rsi[self.element]
        Rse = self.Rse[self.element]
        sumR = sum([l.R() for l in self])+Rsi+Rse
        return 1/sumR

    def thickness(self):
        return sum([l.t for l in self])

    def __str__(self):
        s = 'buildingSurface object: {0}\n'.format(self.name)
        s+= '\t{0:10s} = {1:4.3f}\n'.format('U-value',self.U())
        s+= '\t{0:10s} = {1:4.3f}\n'.format('Thickness',self.thickness())
        return s+'\n'

class building:
    def __init__(self, measures, walls, roof, windows):
        pass

# Overall beam CC

CC=0.60

# Materials definition
Air = material(Lambda=100) # Assume ventilated luftspalt: no contribution
Gips = material(Lambda=0.25)
Wood = material(Lambda=0.14)
FlexiBats = material(Lambda=0.037)
IsoCell = material(Lambda=0.038)
Pevatherm = material(Lambda=0.04)

studs      = component(Wood,width=45e-3)
luftspalt  = component(Air,width=CC-studs.width)
gips       = component(Gips,width=CC)
boards     = component(Wood,width=CC)
isoCell    = component(IsoCell,width=CC-studs.width)
flexiBatts = component(FlexiBats,width=CC-studs.width)
pevatherm  = component(Pevatherm,width=CC)


testWall = buildingSurface(name='Reference wall with known U-value= {0:0.3f}'.format((0.225+0.2113)/2))
testWall.append(layer(thickness=0.013,cc=CC,components=[gips]))
testWall.append(layer(thickness=0.07,cc=CC,components=[flexiBatts,studs]))
testWall.append(layer(thickness=0.12,cc=CC,components=[flexiBatts,studs]))
testWall.append(layer(thickness=0.025,cc=CC,components=[luftspalt,studs],insulation=False))
testWall.append(layer(thickness=0.025,cc=CC,components=[boards],insulation=False))

oldWall = buildingSurface(name='Old walls')
oldWall.append(layer(thickness=0.013,cc=CC,components=[gips]))
oldWall.append(layer(thickness=0.05,cc=CC,components=[boards]))
oldWall.append(layer(thickness=0.03,cc=CC,components=[studs,isoCell]))
oldWall.append(layer(thickness=0.04,cc=CC,components=[studs,luftspalt]))
oldWall.append(layer(thickness=0.03,cc=CC,components=[boards]))
# Addon insulation old walls
oldWall.append(layer(thickness=0.12,cc=CC,components=[studs,isoCell]))
#oldWall.append(layer(thickness=0.025,cc=CC,components=[pevatherm]))
oldWall.append(layer(thickness=0.045,cc=CC,components=[luftspalt,studs]))

newWall = buildingSurface(name='New walls')
newWall.append(layer(thickness=0.013,cc=CC,components=[gips]))
newWall.append(layer(thickness=0.028,cc=CC,components=[boards]))
newWall.append(layer(thickness=0.16,cc=CC,components=[studs,isoCell]))
newWall.append(layer(thickness=0.12,cc=CC,components=[studs,isoCell]))
newWall.append(layer(thickness=0.025,cc=CC,components=[pevatherm]))
newWall.append(layer(thickness=0.045,cc=CC,components=[luftspalt,studs]))

roof = buildingSurface(name='Roof', element='roof')
roof.append(layer(thickness=0.013,cc=CC,components=[gips]))
roof.append(layer(thickness=0.028,cc=CC,components=[boards]))
roof.append(layer(thickness=0.36,cc=CC,components=[isoCell,studs]))
roof.append(layer(thickness=0.028,cc=CC,components=[boards],insulation=False))
roof.append(layer(thickness=0.028*2,cc=CC,components=[studs,luftspalt],insulation=False))

K0roof = buildingSurface(name='K0_Roof', element='roof')
K0roof.append(layer(thickness=0.013,cc=CC,components=[gips]))
K0roof.append(layer(thickness=0.028,cc=CC,components=[boards]))
K0roof.append(layer(thickness=0.145,cc=CC,components=[flexiBatts,studs]))
K0roof.append(layer(thickness=0.220,cc=CC,components=[flexiBatts,studs]))
K0roof.append(layer(thickness=0.035,cc=CC,components=[studs,luftspalt],insulation=False))
K0roof.append(layer(thickness=0.023,cc=CC,components=[boards],insulation=False))

print(testWall)
print('\n')
print(roof)
print(K0roof)
print(oldWall)
print(newWall)


print('\nHouse dimensions:')
print('House wall oldWall area[m2] = {0:3.0f}'.format(House.oldWallsArea()))
print('House wall newWall area[m2] = {0:3.0f}'.format(House.newWallsArea()))
print('House wall total area  [m2] = {0:3.0f}'.format(House.totalWallArea()))
print('House roof area        [m2] = {0:3.0f}'.format(House.roofArea()))
print('House windows area     [m2] = {0:3.0f}'.format(House.totalWindowArea()))

avgDeltaT = 22-(6)
lossRoof = roof.U()*House.roofArea()
lossOldWall = oldWall.U()*House.oldWallsArea()
lossNewWall = newWall.U()*House.newWallsArea()
lossWindows = House.windowsU*House.totalWindowArea()
totalConductionLosses=lossOldWall+lossNewWall+lossRoof+lossWindows

print('')
print('Energy flux calculations at delta T = {0}:'.format(avgDeltaT))
print('Energy flux roof      [W] = {0:3.0f}'.format(lossRoof*avgDeltaT))
print('Energy flux old walls [W] = {0:3.0f}'.format(lossOldWall*avgDeltaT))
print('Energy flux new walls [W] = {0:3.0f}'.format(lossNewWall*avgDeltaT))
print('Energy flux windows   [W] = {0:3.0f}'.format(lossWindows*avgDeltaT))
print('Energy flux total     [W] = {0:3.0f}'.format(totalConductionLosses*avgDeltaT))
print('Overall U-value   [W/m2K] = {0:3.2f}'.format(totalConductionLosses/House.totalHouseArea()))


print('\nVentilation losses:')

ventilationFactor = 0.5
ventilationEfficiency = 0.7
CpAir = 1005.0
rhoAir = 1.2
airFlux = rhoAir*House.volume()*ventilationFactor/3600 # kg/s
energyFlux = CpAir*airFlux*avgDeltaT*(1-ventilationEfficiency)
vPipeDiameter = 0.16
vPipeArea = pi*0.25*vPipeDiameter**2

print('House volume           [m3] = {0:3.0f}'.format(House.volume()))
print('Ventilation factor          = {0}'.format(ventilationFactor))
print('Ventilation air flux [m3/s] = {0:3.2e}'.format(airFlux/rhoAir))
print('Ventilation energy flux [W] = {0:3.0f}'.format(energyFlux))

print('Ventilation pipe diam.  [m] = {0:3.2f}'.format(vPipeDiameter))
print('Ventilation air vel.  [m/s] = {0:3.2f}'.format(airFlux/(rhoAir*vPipeArea)))

print('\nVentilation and conduction loss total:')
totalPower = energyFlux+totalConductionLosses*avgDeltaT
print('Total energy flux       [W] =  {0:3.0f}'.format(totalPower))
print('Total energy budget   [kWh] =  {0:3.0f}'.format(totalPower*1e-3*24*365))
