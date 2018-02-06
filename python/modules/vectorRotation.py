#!/usr/bin/env python

from numpy import *


def toDeg(r):
   return r*180.0/pi
def toRad(d):
   return d*pi/180


class rotationMatrix:
    '''Input rotation in degrees!'''

    def __init__(self,phiX,phiY,phiZ):
        self.phiX=toRad(phiX)
        self.phiY=toRad(phiY)
        self.phiZ=toRad(phiZ)

    def __str__(self):
        return str((self.phiX,self.phiY,self.phiZ))

    def X(self):
       p=self.phiX
       return matrix([[1, 0,        0       ], \
                      [0, cos(p),   -sin(p)  ], \
                      [0, sin(p),  cos(p)  ]])
    def Y(self):
       p=self.phiY
       return matrix([[cos(p),  0, -sin(p) ], \
                      [0,       1, 0      ], \
                      [sin(p), 0, cos(p) ]])
    def Z(self):
       p=self.phiZ
       return matrix([[cos(p),  -sin(p),  0 ], \
                      [sin(p), cos(p),  0 ], \
                      [0,       0,       1 ]])

    def rotate(self,V,order='xyz'):
        funDict={'x':self.X, 'y':self.Y, 'z':self.Z}
        A = matrix(V).transpose()
        for xyz in order:
            A = funDict[xyz]()*A
        return array(A.transpose())[0]

if __name__=="__main__":
    v=[1,1,0.1]
    v=array(v)
    M=rotationMatrix(90,10,80)
    for o in ['xyz','xzy','zxy','zyx','yxz','yzx']:
        print '\n',o
        vr=M.rotate(v,o)
        print v
        print vr
        print 'Vector lengths: ', sqrt(dot(vr,vr)),'==', sqrt(dot(v,v))


