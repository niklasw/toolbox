#!/usr/bin/python
from __future__ import division
import sys
# REF:
# http://www.traguiden.se/konstruktion/dimensionering/berakningsexempel/bostadshus/bjalklag-av-konstruktionsvirke-ej-lagenhetsskiljande/

def funcName():
    import inspect
    return inspect.stack()[1][3]

class material:
    def __init__(self,rho,E,name='unnamed'):
        self.rho = rho
        self.E = E
        self.name = name

    def info(self):
        return '''    Material {0}:
            -------------------
            Density  = {1}
            Youngs E = {2} '''.format(self.name,self.rho,self.E)

    def __str__(self):
        return self.info()

class section(material):
    def __init__(self,mat,b=1,h=1):
        m=mat
        material.__init__(self, m.rho, m.E, m.name)
        self.b=b
        self.h=h

    def E(self):
        return self.E

    def I(self):
        b,h = self.b,self.h
        return b*h**3/12

    def area(self):
        return self.b*self.h

    def EI(self):
        return self.I()*self.E

    def info(self):
        return '''    Section:
        {0}
        B         = {1}
        H         = {2} '''.format(str(self.material),self.b,self.h)

    def __str__(self):
        return self.info()

class rectangularSection(section):
    def __init__(self,*args,**kwargs):
        section.__init__(self,*args,**kwargs)


class beam(section):
    def __init__(self,crossSection,L,origin=(0,0)):
        cs = crossSection
        section.__init__(self,cs,cs.b,cs.h)
        self.L=L
        self.origin = origin

    def uniformLoadDeflection(self,q):
        '''Load q [N/m]'''
        delta = 5.0/384*q*self.L**4/self.EI()
        print('''
            {2}:
                d = {0:0.3e} m
              L/d = {1:0.3f}'''.format(delta,self.L/(delta+1e-6),funcName()))
        print('''
            Load per meter = {0} N
            End loads = {1} N
            End shear stress = {2} MPa
            '''.format(q,self.L*q/2, self.L*q/2/self.area()/1e6))
        return delta

    def centerLoadDeflection(self,p):
        delta = 1.0/48*p*self.L**3/self.EI()
        print('''
            {2}:
                d = {0:0.3e} m
              L/d = {1:0.3f}'''.format(delta,self.L/(delta+1e-6),funcName()))
        print('''
            point load at end = {0} N
            '''.format(p))
        return delta

    def info(self):
        print('''Beam summary:
        L = {0:0.2f}
        b = {1:0.2e}
        h = {2:0.2e}
        E = {3:3.2e}
        I = {4:3.2e}'''.format(self.L,self.b,self.h,self.E, self.I()))

class cantileverBeam(beam):
    def __init__(self,section,L,origin=(0,0)):
        beam.__init__(self,section,L,origin)

    def uniformLoadDeflection(self,q):
        delta = 3.0/24*q*self.L**4/self.EI()
        print('''
            {2}:
                d = {0:0.3e} m
              L/d = {1:0.3f}'''.format(delta,self.L/(delta+1e-6),funcName()))
        print('''
            Load per meter = {0} N
            '''.format(q))
        return delta


    def endLoadDeflection(self,p):
        delta = 1.0/3*p*self.L**3/self.EI()
        print('''
            {2}:
                d = {0:0.3e} m
              L/d = {1:0.3f}'''.format(delta,self.L/(delta+1e-6),funcName()))
        printr('''
            point load at extreme end = {0} N
            '''.format(p))
        return delta

class iBeam(beam):
    def __init__(self,section,L,origin=(0,0)):
        beam.__init__(self,section,L,origin)

    def I(self):
        return 0.0001826

class load:
    def __init__(self,f,x0=0.0,x1=0.0):
        self.x0 = x0
        self.x1 = x1
        self.f = f
        pass


mm = 1e-3

L  =  7.2
cc = 600*mm
bb =  45*mm
bh = 400*mm

Kerto=material(rho=700,E=12e9,name='Kerto')
C24=material(rho=700,E=10e9,name='C24')
limtra=material(rho=700,E=12e9,name='Limtrae')

single145 = rectangularSection(C24,b=bb,h=145*mm)
single170 = rectangularSection(C24,b=bb,h=170*mm)
double170 = rectangularSection(C24,b=2*bb,h=170*mm)
single190 = rectangularSection(C24,b=bb,h=190*mm)
single220 = rectangularSection(C24,b=bb,h=220*mm)

lina1 = beam(single190,2.86)
lina1.info()

q=1e3
p=1e3          #N (point load)

delta  = lina1.uniformLoadDeflection(q)
delta += lina1.centerLoadDeflection(p)

print('Deflection = ',delta)
lina2 = beam(single145,120)
lina2.info()

q=1e3
p=1e3          #N (point load)

delta  = lina1.uniformLoadDeflection(q)
delta += lina1.centerLoadDeflection(p)

print('Deflection = ',delta)

