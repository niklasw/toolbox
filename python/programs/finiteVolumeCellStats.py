#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math,os,sys

class vector:
    '''NOT USED'''
    def __init__(self,l,rads):
        self.length = l
        self.angle = rads
        self.x = l*math.cos(rads)
        self.y = l*math.sin(rads)

class edge:
    '''NOT USED'''
    def __init__(self,L):
        self.length = L

class polygon:
    '''NOT USED.  Equal angled polygons only'''
    def __init__(self,edges):
        self.edges = edges

    def interiorAngle(self):
        return (len(edges)-2)*math.pi/len(edges)

    def totalEdgeLength(self):
        return sum([e.length for e in self.edges])


def mean(alist):
    return float(sum(alist))/len(alist)
#
# Two dimensions -------------------------------------------------------------
#
class triangle(object):
    def __init__(self,l):
        self.L = float(l)
        self.name = '(triangle with side length = {})'.format(self.L)

    def H(self):
        return self.L*math.sqrt(3)/2

    def A(self):
        return 0.5* self.H()*self.L

    def totalEdgeLength(self):
        return 3*self.L

    def insphereRadius(self):
        return 0.5*self.L/math.sqrt(3)

class rectangle(object):
    def __init__(self,l1,l2):
        self.B = float(l1)
        self.H = float(l2)
        self.name = '(rectangle with side lengths = {},{})'.format(self.B,self.H)

    def A(self):
        return self.B*self.H

    def totalEdgeLength(self):
        return 2*(self.B+self.H)

    def insphereRadius(self):
        return math.sqrt(self.B*self.H)*0.5

#
# Three dimensions ------------------------------------------------------------
#
class cell(object):

    def __init__(self):
        pass

    def cubeRootVolDelta(self):
        return self.V()**(1./3.)

    def VtoADelta(self, C=6.0):
        return C*self.V()/self.A()

    def __str__(self):
        s = '\n'+self.name
        s += '\n volume           = {} m3'.format(self.V())
        s += '\n face area        = {} m2'.format(self.A())
        s += '\n volume/area      = {} m'.format(self.V()/self.A())
        s += '\n cells per m3     = {} m'.format(1.0/self.V())
        s += '\n faces per m3     = {} m'.format(1.0/self.V()*len(self.faces))
        s += '\n CC distance      = {} m'.format(self.insphereRadius()*2)
        s += '\n LES V^1/3 Delta  = {}'.format(self.cubeRootVolDelta())
        s += '\n LES VtoA  Delta  = {}'.format(self.VtoADelta())
        return s


class prism(cell):
    def __init__(self,t,h):
        cell.__init__(self)
        self.base = t
        self.height = h
        if self.base.__class__.__name__ == 'triangle':
            self.side0 = rectangle(t.L,h)
            self.side1 = self.side0
            self.faces = 3*(self.side0,)+2*(self.base,)
        elif self.base.__class__.__name__=='rectangle':
            self.side0 = rectangle(t.B,h)
            self.side1 = rectangle(t.H,h)
            self.faces = 2*(self.base,)+2*(self.side0,)+2*(self.side1,)
        self.name = '(prism of {} with height {})'.format(self.base.name,self.height)

    def V(self):
        return self.base.A()*self.height

    def A(self):
        #return 2*self.base.A()+self.base.totalEdgeLength()*self.height
        return sum([f.A() for f in self.faces])

    def insphereRadius(self):
        return self.base.insphereRadius()

class tet(cell):
    def __init__(self,t):
        cell.__init__(self)
        self.face = t
        self.faces = 4*(self.face,)
        self.name = '(tetrahedron of faces {})'.format(self.face.name)

    def H(self):
        return (1.0/3)*math.sqrt(6)*self.face.L

    def V(self):
        return 1/3.0*self.face.A()*self.H()

    def A(self):
        return sum([face.A() for face in self.faces])

    def insphereRadius(self):
        return self.face.L/12.*math.sqrt(6)


class hex(cell):
    def __init__(self,b1,b2):
        cell.__init__(self)
        self.face1 = b1
        self.face2 = b2
        self.face3 = rectangle(b1.B,b2.B)
        self.faces = (b1,b2,self.face3,b1,b2,self.face3)
        self.name = '(hexahedron of faces {},{})'.format(b1.name,b2.name)

    def V(self):
        return self.face1.A()*self.face2.H

    def A(self):
        return sum([face.A() for face in self.faces])

    def insphereRadius(self):
        return mean([f.insphereRadius() for f in self.faces])

if len(sys.argv) != 4:
    prog = os.path.basename(sys.argv[0])
    print "Usage: {0} <rectangle length> <triangle length> <prism height>".format(prog)
    sys.exit(1)

rectSide = float(sys.argv[1])
triSide = float(sys.argv[2])
height = float(sys.argv[3])

h=height

T = triangle(triSide)
R = rectangle(rectSide,rectSide)

Tprism = prism(T,h)
Hprism = prism(R,h)
Tet = tet(T)
Hex = hex(R,R)

print Tprism
print Hprism
print Tet
print Hex

