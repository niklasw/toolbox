#!/usr/bin/python

import sys
from math import *
import numpy as np
import matplotlib.pyplot as plt

savefig = False
if len(sys.argv) == 2:
    if sys.argv[1] == 'save':
        savefig = True

fsize = 32

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
        plt.xlabel('x', fontsize=fsize)
        plt.ylabel('y', fontsize=fsize)
        plt.xlim(self.x0, self.x1)
        plt.ylim(self.y0, self.y1)
        plt.scatter(self.X, self.Y, color='#CD2305', s=8, marker='o')

class source:
    def __init__(self,strength,x,y,Mesh):
        self.strength = strength
        self.x = x
        self.y = y
        self.r = Mesh.R(self.x,self.y)
        self.X = Mesh.X - self.x
        self.Y = Mesh.Y - self.y
        self.mesh = Mesh

    def potential(self):
        r = self.r
        return -self.strength/(4*pi*r) ##- Sign?

    def velocity(self):
        r3 = self.r**3
        u = self.strength/(4*pi) * self.X/r3
        v = self.strength/(4*pi) * self.Y/r3
        return (u,v)

    def streamFunction(self):
        r = self.r
        #return self.strength/(4*pi) * (1.0-self.X/(4*pi*r))
        return self.strength/(2*pi)*np.arctan2(self.mesh.Y,self.X)

class freeStream:
    def __init__(self,U,V,Mesh):
        self.mesh = Mesh
        self.u = U
        self.v = V

    def potential(self):
<<<<<<< HEAD
        self.phi = 0.5*U*self.mesh.Y**2

    def velocity(self):
        pass

    def streamFunction(self):
        pass
=======
        return self.mesh.X*self.u
>>>>>>> 09bd5111fe1eccf37120fa1d28ad8cd744adc9f2

    def velocity(self):
        return (self.u,self.v)

    def streamFunction(self):
        return self.mesh.Y*self.u

class sourceList(list):
    def __init__(self, Mesh):
        list.__init__(self)
        self.mesh = Mesh
        self.fs = freeStream(0,0,Mesh)

    def potential(self):
        phi = 0.0
        for s in self:
            phi += s.potential()
        return phi

    def velocity(self):
        u,v = self.fs.velocity()
        for s in self:
            u += s.velocity()[0]
            v += s.velocity()[1]
        return (u,v)

    def streamFunction(self):
        psi = self.fs.streamFunction()
        for s in self:
            psi += s.streamFunction()
        return psi

    def addSource(self,strength, x, y):
        self.append(source(strength,x,y,self.mesh))

    def addFreeStream(self,U,V):
        self.fs = freeStream(U,V,self.mesh)

    def getCp(self):
        u,v = self.velocity()
        return 1.0 - (u**2+v**2)/self.fs.u**2

class rankineBody:
    def __init__(self, sources):
        self.sources = sources
        self.fs = sources.fs

    def solveDimensions(self, guess):
        '''Iteratively solve for Rankine body
        dimensions according to equations in Shaffer
        page 3'''
        strength = self.sources[0].strength
        U = self.fs.u
        c = abs(self.sources[0].x)
        M=strength/(4*pi)

        K = c*M/(U*pi)

        def lRHS(d,K):
            d2 = c**2+sqrt(d*K)
            return sqrt(d2)

        def hRHS(d,K):
            d2 = K/sqrt(d**2+c**2)
            return sqrt(d2)

        def solve(f,K,init):
            d=init
            d0=d+1
            for i in range(50):
                d = f(d0,K)
                if abs(d0-d) < 1e-6:
                    return 2*d
                d0=d

            print "WARNING: Solver did not converge"
            return 0.0

        w = solve(hRHS,K,guess/5.0)
        l = solve(lRHS,K,guess)

        return l,w

    def Froude(self,L,g=9.81):
        U = sqrt(self.fs.u**2+self.fs.v**2)
        Fr =  U/sqrt(g*L)
        print 'Depth Froude number = {0:3.2f}'.format(Fr)
        return U/sqrt(g*L)

    def waves(self, depth, distance, g=9.81):
        '''Wave pattern along surface center line
        according to Shaffer/Yim'''
        # Divide by 4p? Depending on wether Shaffer is consistent
        # regarding the source notation M or not.
        M = abs(float(self.sources[0].strength) / (4*pi))
        f = abs(float(depth))
        c = abs(float(self.sources[0].x))
        U = abs(self.fs.u)
        Fr = self.Froude(f)
        B = 8*M/(f**2*U*Fr) * exp(-1/Fr**2) * sin(c/(f*Fr**2))
        h2f = lambda R: B*sqrt(2*pi*f/R) * sin(R/(f*Fr**2) - 3*pi/4)

        return [f*h2f(R) for R in distance ]

    def singleSourceWaves(self,depth,distance,sourceId=0,g=9.81):
        '''Wave pattern from a single source moving beneath
        a free surface  according to Shaffer/Yim'''
        source = self.sources[sourceId]
        M = abs(float(source.strength) / (4*pi))
        f = abs(float(depth))
        c = abs(float(source.x))
        offset = float(source.x)
        U = abs(self.fs.u)

        h = lambda sign,R: sign*4*M/U*sqrt(2*pi*g/(R*U**2))*exp(-g*f/U**2)*cos(g*R/U**2+pi/4)
        return np.array([h(1.0,R-offset) for R in distance ])

    def getWaveLength(self,g=9.81):
        '''Wave length according to Shaffer/Yim'''
        return 2*pi*self.fs.u**2/g

    def plotWaves(self,depth,distance):
        #wh = self.waves(depth,distance)
        wh = self.singleSourceWaves(depth,distance,0)
        wh+= self.singleSourceWaves(depth,distance,1)

        plt.title('Waves along center line above body', fontsize=fsize)
        plt.xlabel('Distance', fontsize=fsize)
        plt.ylabel('Centerline surface elevation', fontsize=fsize)
        plt.plot(distance,wh)
        plt.grid('on')
        plt.xlim(-2,np.max(distance))
        plt.ylim(-2*np.max(wh[len(wh)/2:]),2*np.max(wh[len(wh)/2:]))

        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

        return wh


class canvas:
    def __init__(self,sources):
        self.sources = sources

    def new(self, size):
        plt.figure(figsize=size)

    def plotStreamlines(self):
        plt.title('Streamlines',fontsize=fsize)
        plt.grid(True)
        plt.xlabel('x', fontsize=fsize)
        plt.ylabel('y', fontsize=fsize)
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        u,v = self.sources.velocity()
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        plt.streamplot(X, Y, u, v, density=2, color='#888888', linewidth=1, arrowsize=1, arrowstyle='->')
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

    def plotStreamfunction(self):
        plt.title('Streamfunction',fontsize=fsize)
        plt.grid(True)
        plt.xlabel('x', fontsize=fsize)
        plt.ylabel('y', fontsize=fsize)
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        u,v = self.sources.velocity()
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        strf = self.sources.streamFunction()

        plt.contour(X, Y, strf, levels=np.linspace(strf.min(),strf.max(),21),extend='both')
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

    def plotPotential(self):
        plt.title('Potential',fontsize=fsize)
        plt.grid(True)
        plt.xlabel('x', fontsize=fsize)
        plt.ylabel('y', fontsize=fsize)
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        contf = plt.contourf(X, Y, self.sources.potential(), levels=np.linspace(-4.0, 4.0, 100), extend='both')
        plt.contour(X, Y, self.sources.potential(), levels=[-1,0,1],extend='both',linestyles='dashed',linewidths=2,colors='#000000')
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

    def plotCp(self):
        plt.title('Pressure coefficient, $C_p$',fontsize=fsize)
        plt.grid(True)
        plt.xlabel('x', fontsize=fsize)
        plt.ylabel('y', fontsize=fsize)
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        contf = plt.contourf(X, Y, self.sources.getCp(), levels=np.linspace(-2.0, 1.0, 100), extend='both')
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')
        cbar = plt.colorbar(contf)
        cbar.set_label('$C_p$', fontsize=fsize)
        cbar.set_ticks([-2.0, -1.0, 0.0, 1.0])

    def plotBody(self, line='solid'):
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        plt.contour(X, Y, self.sources.streamFunction(), levels= [0.0], colors='#CD2305', linewidths=2, linestyles=line)

def feet2m(l):
    return l*0.3048
def m2feet(m):
    return m/0.3048

if __name__ == '__main__':

    u_inf = 3.048    # 10 feet/s    Shaffer page 13
    x_offset = 1.274 # 4.18 ft from Shaffer page 5
    y_offset = 0.0

    # depthFactor  = 2.0          # Centerline depth is body diameter x depthFactor
    clDepth      = 0.9144         # 3 feet    Shaffer page 13
    sourceFactor = 0.104*(4*pi)   # From page 5 in Shaffer ( 4*pi ??)

    sourceStrength = u_inf * sourceFactor

    Mesh = mesh(-1.5*x_offset,1.5*x_offset,-1*x_offset, 1*x_offset,300,200)

    Sources = sourceList(Mesh)
    Sources.addSource( sourceStrength, -x_offset, y_offset)
    Sources.addSource(-sourceStrength,  x_offset, y_offset)
    Sources.addFreeStream(u_inf,0)

    size = 15
    figureSize = (size, (Mesh.dimensions()[1])/(Mesh.dimensions()[0])*size)

    c = canvas(Sources)

    c.new(figureSize)
    c.plotStreamlines()
    c.plotStreamfunction()
    c.plotBody(line='dashed')

    c.new(figureSize)
    c.plotPotential()
    c.plotBody(line='dashed')

    c.new(figureSize)
    c.plotCp()
    c.plotBody(line='dashed')

    # -Rankine Body ----------------------------------
    body = rankineBody(Sources)

    wl =  body.getWaveLength()
    print 'Wave length = ',wl


    l,w = body.solveDimensions(guess=1.0)
    print 'Velocity    = {0:8.2f} m/s, {1:8.2f} f/s'.format(u_inf,m2feet(u_inf))
    print 'Src offset  = {0:8.2f} m, {1:8.2f} f'.format(x_offset,m2feet(x_offset))
    print 'Body Lpp    = {0:8.2f} m, {1:8.2f} feet'.format(l,m2feet(l))
    print 'Body w      = {0:8.2f} m, {1:8.2} feet'.format(w,m2feet(w))
    print 'Body aspect = {0:8.2f}'.format(l/w)
    print 'Cl depth    = {0:8.2f} m, {1:8.2f} feet'.format(clDepth,m2feet(clDepth))

    plt.figure(figsize=figureSize)
    wh = body.plotWaves(clDepth, np.linspace(x_offset+0.1,8*wl,400))
    # ------------------------------------------------

    plt.show()
