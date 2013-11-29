#!/usr/bin/env python

from numpy import *


def toDeg(r):
   return r*180.0/pi
def toRad(d):
   return d*pi/180


class rotationMatrix:

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

    def rotate(self,V):
        A = matrix(V).transpose()
        A = self.X()*A
        A = self.Y()*A
        A = self.Z()*A
        return array(A.transpose())[0]

if __name__=="__main__":
    v=[1,1,1]
    M=rotationMatrix(0,90,-90)
    vr=M.rotate(v)
    v=array(v)
    print vr,v
    print sqrt(dot(vr,vr)), sqrt(dot(v,v))


