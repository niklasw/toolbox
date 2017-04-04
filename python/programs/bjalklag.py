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
        return b*h

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
        print '''
            {2}:
                d = {0:0.3e} m
              L/d = {1:0.3f}'''.format(delta,self.L/(delta+1e-6),funcName())
        print '''
            Load per meter = {0} N
            '''.format(q)
        return delta

    def centerLoadDeflection(self,p):
        delta = 1.0/48*p*self.L**3/self.EI()
        print '''
            {2}:
                d = {0:0.3e} m
              L/d = {1:0.3f}'''.format(delta,self.L/(delta+1e-6),funcName())
        print '''
            point load at end = {0} N
            '''.format(p)
        return delta

    def info(self):
        print '''Beam summary:
        L = {0:0.2f}
        b = {1:0.2e}
        h = {2:0.2e}
        E = {3:3.2e}
        I = {4:3.2e}'''.format(self.L,self.b,self.h,self.E, self.I())

class cantileverBeam(beam):
    def __init__(self,section,L,origin=(0,0)):
        beam.__init__(self,section,L,origin)

    def uniformLoadDeflection(self,q):
        delta = 3.0/24*q*self.L**4/self.EI()
        print '''
            {2}:
                d = {0:0.3e} m
              L/d = {1:0.3f}'''.format(delta,self.L/(delta+1e-6),funcName())
        print '''
            Load per meter = {0} N
            '''.format(q)
        return delta


    def endLoadDeflection(self,p):
        delta = 1.0/3*p*self.L**3/self.EI()
        print '''
            {2}:
                d = {0:0.3e} m
              L/d = {1:0.3f}'''.format(delta,self.L/(delta+1e-6),funcName())
        print '''
            point load at extreme end = {0} N
            '''.format(p)
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

kerto360 = rectangularSection(Kerto,bb,bh)
kerto300 = rectangularSection(Kerto,bb,300*mm)
double170 = rectangularSection(C24,2*bb,170*mm)
limbalk1 = rectangularSection(limtra,90*mm,270*mm)
limbalk2 = rectangularSection(limtra,56*mm,270*mm)

golvBalk = beam(kerto360,L)
golvBalk.info()

Qe = 0.85e3    # N/m2 egentyngd
Q  = 2.0e3     # N/m2 2000 enl lastkategori A
q=(Q+Qe)*cc    # N/m
q_save = q
p=1e3          #N (point load)

delta = golvBalk.uniformLoadDeflection(q)
delta = golvBalk.centerLoadDeflection(p)

print 'Takkupans balk'

L=3.65
B=4.0
Area=L*B
Load=Area*(Q+Qe)*0.5
q=Load/L

kupBalk = beam(double170,L)
kupBalk.info()
kupBalk.uniformLoadDeflection(q)

print 30*'='

# Laster Balkong
p  = 0000
q  = 2000

print 'Yttre Balkongbalk'
balkong1 = cantileverBeam(limbalk1,2.5)
balkong1.info()
delta = balkong1.uniformLoadDeflection(q)
delta+= balkong1.endLoadDeflection(p)
print 'Total deflection = ', delta

balkong2 = cantileverBeam(limbalk2,1.4)
balkong2.info()
delta = balkong2.uniformLoadDeflection(q)
delta+= balkong2.endLoadDeflection(p)
print 'Total deflection = ', delta
