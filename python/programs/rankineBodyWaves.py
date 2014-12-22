#!/usr/bin/python

import sys
from math import *
import numpy as np
import matplotlib.pyplot as plt

class mesh:
    def __init__(self,x0,x1,y0,y1,Nx,Ny):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.Nx = Nx
        self.Ny = Ny

        self.info()

        self.generate()

    def info(self):
        print 'Mesh stats:'
        for a,v in self.__dict__.iteritems():
            print '\t{0}   =    {1}'.format(a,v)
        print ''

    def generate(self):
        x = np.linspace(self.x0, self.x1, self.Nx)
        y = np.linspace(self.y0, self.y1, self.Ny)
        self.X, self.Y = np.meshgrid(x, y)

    def R(self,x,y):
        return np.sqrt((self.X-x)**2+(self.Y-y)**2)

    def dimensions(self):
        return [self.x1-self.x0, self.y1-self.y0]

    def plot(self):
        plt.xlabel('x', fontsize=16)
        plt.ylabel('y', fontsize=16)
        plt.xlim(self.x0, self.x1)
        plt.ylim(self.y0, self.y1)
        plt.scatter(self.X, self.Y, color='#CD2305', s=8, marker='o')


class source:
    def __init__(self,strength,x,y,Mesh):
        self.x = x
        self.y = y
        self.strength = strength
        self.mesh = Mesh
        self.r = Mesh.R(self.x,self.y)
        self.X = self.mesh.X - self.x
        self.Y = self.mesh.Y - self.y

        self.potential()
        self.velocity()
        self.streamFunction()

    def potential(self):
        r = self.r
        self.phi = self.strength/(4*pi*r)

    def velocity(self):
        r = self.r
        self.u = self.strength/(4*pi) * self.X/(4*pi*r**3)
        self.v = self.strength/(4*pi) * self.Y/(4*pi*r**3)

    def streamFunction(self):
        r = self.r
        self.psi = self.strength/(4*pi) * (1.0-self.X/(4*pi*r))

class freeStream:
    def __init__(self,U,V,Mesh):
        self.psi = 0.5*U*Mesh.Y**2
        self.phi = U*Mesh.X
        self.u = U
        self.v = V


class rankineBody:
    def __init__(self, fs, sources):
        self.fs = fs
        self.sources = sources
        self.mesh = sources[0].mesh

        self.streamFunction()
        self.potential()
        self.velocity()

    def streamFunction(self):
        self.psi = self.fs.psi
        for s in self.sources:
            self.psi += s.psi

    def potential(self):
        self.phi = self.fs.phi
        for s in self.sources:
            self.phi += s.phi

    def velocity(self):
        self.u = self.fs.u
        self.v = self.fs.v
        for s in self.sources:
            self.u += s.u
            self.v += s.v

    def getCp(self):
        return 1.0 - (self.u**2+self.v**2)/self.fs.u**2

    def solveDimensions(self, guess):
        strength = self.sources[0].strength
        U = self.fs.u
        c = abs(self.sources[0].x)
        M=strength/(4*pi)

        def solveWidth():
            h = guess/5
            h0 = h+1
            while abs(h-h0) > 1e-9:
                h0 = h
                h2 = 2*c*M/(sqrt(h0**2+c**2)*2*pi*U)
                h = sqrt(abs(h2))
            return 2*h

        def solveLength():
            l = guess
            l0 = l+1
            while abs(l-l0) > 1e-9:
                l0 = l
                l2 = sqrt(c*l0*M/(pi*U))+c**2
                l = sqrt(abs(l2))
            return 2*l

        w = solveWidth()
        l = solveLength()
        return l,w

    def Froude(self,L,g=9.81):
        U = sqrt(self.fs.u**2+self.fs.v**2)
        return U/sqrt(g*L)

    def waves(self, depth, distance, g=9.81):
        '''Wave pattern along surface center line
        according to Shaffer/Yim'''
        M = float(self.sources[0].strength) / (4*pi)
        f = float(depth)
        c = float(self.sources[0].x)
        U = self.fs.u
        Fr = self.Froude(depth)
        B = 8*M/(f**2*U*Fr) * exp(-1/Fr**2) * sin(c/(f*Fr**2))
        h2f = lambda R: B*sqrt(2*pi*f/R) * sin(R/(f*Fr**2) - 3*pi/4)

        return [f*h2f(R) for R in distance ]

    def getWaveLength(self,g=9.81):
        '''Wave length according to Shaffer/Yim'''
        return 2*pi*self.fs.u**2/g

    def plotStreamlines(self):
        plt.title('Stream function')
        plt.grid(True)
        plt.xlabel('x', fontsize=16)
        plt.ylabel('y', fontsize=16)
        X = self.mesh.X
        Y = self.mesh.Y
        u = self.u
        v = self.v
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        plt.streamplot(X, Y, u, v, density=2, linewidth=1, arrowsize=1, arrowstyle='->')
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

    def plotPotential(self):
        plt.title('Potential')
        plt.grid(True)
        plt.xlabel('x', fontsize=16)
        plt.ylabel('y', fontsize=16)
        X = self.mesh.X
        Y = self.mesh.Y
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        contf = plt.contourf(X, Y, self.phi, levels=np.linspace(-4.0, 4.0, 100), extend='both')
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

    def plotCp(self):
        plt.title('Pressure coefficient, $C_p$')
        plt.grid(True)
        plt.xlabel('x', fontsize=16)
        plt.ylabel('y', fontsize=16)
        X = self.mesh.X
        Y = self.mesh.Y
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        contf = plt.contourf(X, Y, self.getCp(), levels=np.linspace(-2.0, 1.0, 100), extend='both')
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')
        cbar = plt.colorbar(contf)
        cbar.set_label('$C_p$', fontsize=16)
        cbar.set_ticks([-2.0, -1.0, 0.0, 1.0])


    def plotBody(self, line='solid'):
        X = self.mesh.X
        Y = self.mesh.Y
        plt.contour(X, Y, self.psi, levels= [0.0], colors='#CD2305', linewidths=2, linestyles=line)

    def plotWaves(self,depth,distance):
        wh = self.waves(depth,distance)
        plt.title('Waves along center line above body')
        plt.xlabel('Distance')
        plt.ylabel('Centerline surface elevation')
        plt.plot(distance,wh)
        plt.grid('on')
        plt.xlim(0,np.max(distance))
        plt.ylim(-1.1*np.max(wh),1.1*np.max(wh))
        return wh


def feet(l):
    return l*0.3048

if __name__ == '__main__':

    u_inf = 3
    x_offset = 1.4
    y_offset = 0.0
    depthFactor  = 2.0
    sourceFactor = 0.104*(4*pi)

    sourceStrength = u_inf * sourceFactor

    Mesh = mesh(-1.5*x_offset,1.5*x_offset,-1*x_offset, 1*x_offset,300,200)

    Sources = []
    Sources.append( source( sourceStrength, -x_offset, y_offset, Mesh) )
    Sources.append( source(-sourceStrength,  x_offset, y_offset, Mesh) )

    FS = freeStream(u_inf,0,Mesh)

    body = rankineBody(FS,Sources)

    l,w = body.solveDimensions(guess=1.0)
    print 'Body Lpp    = ',l
    print 'Body w      = ',w
    print 'Body aspect = ',l/w
    print 'Cl depth    = ', depthFactor*w

    wl =  body.getWaveLength()
    print 'Wave length = ',wl

    size = 15
    figureSize = (size, (Mesh.dimensions()[1])/(Mesh.dimensions()[0])*size)

    plt.figure(figsize = figureSize)
    body.plotStreamlines()
    body.plotBody()

    plt.figure(figsize = figureSize)
    body.plotPotential()
    body.plotBody(line='dashed')
    plt.figure(figsize = figureSize)
    body.plotCp()
    body.plotBody(line='dashed')

    plt.figure(figsize = figureSize)
    wh = body.plotWaves(depthFactor*w, np.linspace(0.1,8*wl,400))

    plt.show()
