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
       return matrix([[cos(p),  0, sin(p) ], \
                      [0,       1, 0      ], \
                      [-sin(p), 0, cos(p) ]])
    def Z(self):
       p=self.phiZ
       return matrix([[cos(p),  -sin(p),  0 ], \
                      [sin(p), cos(p),  0 ], \
                      [0,       0,       1 ]])

    def rotate(self,V,order='xyz'):
        funDict={'x':self.X, 'y':self.Y, 'z':self.Z}
        A = matrix(V).transpose()
        print(A)
        for xyz in order:
            A = funDict[xyz]()*A
        return array(A.transpose())[0]

class projectionRotationMatrix:
    '''Rotation matrix given two colocated coordinate systems defined
    by axes0 and axes1. To project points from one coord-sys to
    another. axes defined as e.g. ((1 0 0) (0 1 0) 0 0 1))'''

    def __init__(self, axes0, axes1):
         self.ax0 = axes0
         self.ax1 = axes1
         self.R = matrix(zeros(9)).reshape(3,3)
         self._fillMatrix()
         print(self.R)
    
    def _fillMatrix(self):
        R = self.R
        x0 = self.ax0
        x1 = self.ax1

        R[0] = [dot(x1[0],v2) for v2 in x0] 
        R[1] = [dot(x1[1],v2) for v2 in x0] 
        R[2] = [dot(x1[2],v2) for v2 in x0] 

    def rotate(self,v):
        return array(self.R.dot(v))[0]

def tryRotationMatrix(v=[0,1,0]):
    v=array(v)
    M=rotationMatrix(90,0,0)
    for o in ['xyz','xzy','zxy','zyx','yxz','yzx']:
        print('\n',o)
        vr=M.rotate(v,o)
        print(v)
        print(vr)
        print('Vector lengths: ', sqrt(dot(vr,vr)),'==', sqrt(dot(v,v)))

def tryProjectionRotationMatrix():
    x0=((1,0,0),(0,1,0),(0,0,1))
    x1=((0,0,1),(0,1,0),(-1,0,0))
    R=projectionRotationMatrix(x0,x1)
    v0 = (1,0,0)
    v1 = R.rotate(v0)
    print(f'Rotating {v0} to {v1}')


if __name__=="__main__":
    tryRotationMatrix([1,0,0])

