#!/usr/bin/python

from __future__ import division

from numpy import array,pi,sqrt,arange,linspace,meshgrid
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm



class WigleyHull:

    def __init__(self,B,L,T,resolution=(4,3)):
        self.B = B
        self.L = L
        self.T = T
        self.x = linspace(0,L/2.0,resolution[0])
        self.z = linspace(0,T,resolution[1])
        self.mesh = meshgrid(self.x,self.z)

    def X(self):
        return self.mesh[0]

    def Z(self):
        return self.mesh[1]

    def Y(self):
        B = self.B
        L = self.L
        T = self.T
        X = self.X()
        Z = self.Z()
        return B/2*(1-(2*X/L)**2)*(1-(Z/T)**2)

    def y(self,x,z):
        B = self.B
        L = self.L
        T = self.T
        return B/2*(1-(2*x/L)**2)*(1-(z/T)**2)

    def plot(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        surface = ax.plot_surface(self.X(), self.Y(), self.Z(),rstride=5,cstride=5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
#        ax.set_aspect('equal')
        plt.show()

    def scipyDisplacement(self):
        from scipy import integrate
        Xrange = [0,self.L/2]
        Zrange = [0,self.T]
        I = integrate.nquad(self.y,[Xrange,Zrange])
        return I[0]

    def analyticalDisplacement(self):
        return self.L*self.B*self.T/9

    def analyticalArea(self):
        B,L,T=self.B,self.L,self.T
        return 4*B**2*(4*T**2+L**2)/(45*T*L)
        

    def createObj(self):
        import copy
        nz,nx = self.X().shape
        print nx,nz
        faces = list()
        verts = list()
        nFaces = (nx-1)*(nz-1)
        for j in range(nz):
            z = self.z[j]
            for i in range(nx):
                x = self.x[i]
                vert = [x, self.y(x,z), z]
                verts.append(vert)
                if i < nx-1 and j < nz-1:
                    face = [nx*j+i+1, nx*j+i+2, nx*j+i+nx+2,  nx*j+i+nx+1]
                    faces.append(face)

        with open('WigleyQuarterHull.obj','w') as obj:
            obj.write('g WigleyHull\n')
            for v in verts:
                obj.write('v {0[0]:10.8f} {0[1]:10.8f} {0[2]:10.8f}\n'.format(v))
            for f in faces:
                obj.write('f {0[0]} {0[1]} {0[2]} {0[3]}\n'.format(f))

if __name__ == '__main__':

    L = 4.0 
    T = L*0.0625
    B = L*0.1

    rez = 500

    hull = WigleyHull(B,L,T,resolution=(rez,int(rez*T*2/L)))

    print 'Numerical Quarter Hull Displacement = ', hull.scipyDisplacement()
    print 'Analytical Quarter Hull Displacement= ', hull.analyticalDisplacement()
    print 'Analytical Quarter Hull Area        = ', hull.analyticalArea()

    hull.createObj()

    #hull.plot()

