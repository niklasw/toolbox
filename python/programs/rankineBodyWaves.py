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
        self.deltas = [0,0]

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
        self.deltas[0] = x[1]-x[0]
        self.deltas[1] = y[1]-y[0]
        self.X, self.Y = np.meshgrid(x, y, indexing='xy')

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
        return -self.strength/(4*pi*r)

    def velocityAlt(self):
        '''Velocity from analytical expression'''
        r3 = self.r**3
        u = self.strength/(4*pi) * self.X/r3
        v = self.strength/(4*pi) * self.Y/r3
        return (u,v)

    def velocity(self):
        '''Velocity from gradient of potential'''
        dx, dy = self.mesh.deltas
        u,v = np.gradient(self.potential(),dx,dy)
        return (v,u) # reversed, due to indexing...

    def streamFunction(self):
        return self.strength/(2*pi)*np.arctan2(self.Y,self.X)

class freeStream:
    def __init__(self,U,V,Mesh):
        self.mesh = Mesh
        self.u = U
        self.v = V

    def potential(self):
        return self.mesh.X*self.u

    def velocityAlt(self):
        '''Velocity from analytical expression'''
        U = np.ones(self.mesh.X.shape)*self.u
        V = np.ones(self.mesh.X.shape)*self.v
        return (U,V)

    def velocity(self):
        '''Velocity from gradient of potential'''
        dx, dy = self.mesh.deltas
        u,v = np.gradient(self.potential(),dx,dy)
        return (v,u)

    def streamFunction(self):
        return self.mesh.Y*self.u

class sourceList(list):
    def __init__(self, Mesh):
        list.__init__(self)
        self.mesh = Mesh
        self.fs = freeStream(0,0,Mesh)

    def potential(self):
        phi = self.fs.potential()
        for s in self:
            phi += s.potential()
        return phi

    def velocity(self):
        u,v = self.fs.velocity()
        for s in self:
            u += s.velocity()[0]
            v += s.velocity()[1]
        return (u,v)

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
        if (abs(self.fs.u) > 0) or (abs(self.fs.v) > 0):
            return 1.0 - (u**2+v**2)/self.fs.u**2
        else:
            return np.zeros(self.mesh.X.shape)

class rankineBody:
    def __init__(self, sources, depth, g=9.81):
        self.sources = sources
        self.fs = sources.fs
        self.depth = depth
        self.g = g
        self.length = 0.0
        self.width = 0.0

    def ok(self):
        '''Just a method to turn of rankine body calculations
        if not all parameters are available, e.g. lacking
        freestream'''
        return ((len(self.sources) == 2) and (self.fs.u != 0))

    def solveDimensions(self, guess):
        '''Iteratively solve for Rankine body
        dimensions according to equations in Shaffer
        page 3'''
        if self.fs.u == 0:
            print 'WARNING: cannot solveDimensions. U=0'
            return 1.0,1.0
        M = self.sources[0].strength
        U = self.fs.u
        c = abs(self.sources[0].x)

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
            return 1.0,1.0

        w = solve(hRHS,K,guess/5.0)
        l = solve(lRHS,K,guess)
        self.length = l
        self.width = w

    def Froude(self,L):
        g = self.g
        U = sqrt(self.fs.u**2+self.fs.v**2)
        Fr =  U/sqrt(g*L)
        return U/sqrt(g*L)

    def waves_combined(self, distance):
        '''Wave pattern along surface center line above a
        Rankine body, according to Shaffer/Yim'''
        M = abs(self.sources[0].strength)# * (4*pi)
        f = abs(self.depth)
        c = abs(self.sources[0].x)
        U = abs(self.fs.u)
        Fr = self.Froude(f)
        B = 8*M/(f**2*U*Fr) * exp(-1/Fr**2) * sin(c/(f*Fr**2))

        R = lambda d: sqrt(f**2 + (d-c)**2)

        h2f = lambda r: B*sqrt(2*pi*f/r) * sin(r/(f*Fr**2) - 3*pi/4)

        return [f*h2f(R(d)) for d in distance ]

    def waves(self,distance):
        '''Superposition of waves from all sources
        '''
        wh = np.zeros(len(distance))
        for S in self.sources:
            wh += self.singleSourceWaves(distance,S)
        return wh
        #return self.waves_combined(distance)

    def singleSourceWaves(self,distance,source):
        '''Wave pattern from a single source moving beneath
        a free surface  according to Shaffer/Yim'''
        M = source.strength
        f = abs(self.depth)
        c = source.x
        U = abs(self.fs.u)
        g = self.g
        print "Source strength factor (from Shaffer) = ", M/U

        # Function to calculate distance to source from downstream
        # distance and depth (Pythagora)
        R = lambda d: sqrt(f**2 + (d-c)**2)

        # Function of r (distance to source) to calculate surface elevation
        # from a single source, according to Shaffer and Yim
        h = lambda r: 4*M/U*sqrt(2*pi*g/(r*U**2))*exp(-g*f/U**2)*cos(g*r/U**2+pi/4)

        return np.array([h(R(d)) for d in distance ])

    def getWaveLength(self,g=9.81):
        '''Wave length'''
        return 2*pi*self.fs.u**2/g

    def plotWaves(self,distance):
        wh = self.waves(distance)
        # wh2= self.waves_combined(distance)

        plt.plot(distance,wh,'g')
        #plt.plot(distance-1.36,wh2,'g')

        plt.title('Waves along center line above body', fontsize=fsize)
        plt.xlabel('Distance', fontsize=fsize)
        plt.ylabel('Centerline surface elevation', fontsize=fsize)
        plt.grid('on')
        plt.xlim(-2,np.max(distance))
        #plt.ylim(-2*np.max(wh[len(wh)/2:]),2*np.max(wh[len(wh)/2:]))

        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

        return wh

    def info(self):
        c = abs(self.sources[0].x)
        print 'Velocity    = {0:8.2f} m/s, {1:8.2f} f/s'.format(self.fs.u,m2f(self.fs.u))
        print 'Src offset  = {0:8.2f} m, {1:8.2f} f'.format(c,m2f(c))
        print 'Body Lpp    = {0:8.2f} m, {1:8.2f} feet'.format(self.length,m2f(self.length))
        print 'Body w      = {0:8.2f} m, {1:8.2} feet'.format(self.width,m2f(self.width))
        print 'Body aspect = {0:8.2f}'.format(self.length/self.width)
        print 'Cl depth    = {0:8.2f} m, {1:8.2f} feet'.format(self.depth,m2f(self.depth))
        print 'Froude(d)   = {0:8.2f}'.format(self.Froude(self.depth))

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

        pot = self.sources.potential()
        maxPot = np.max(self.sources.potential())
        minPot = np.min(self.sources.potential())

        contf = plt.contourf(X, Y, self.sources.potential(), levels=np.linspace(minPot,maxPot,100), extend='both')
        #plt.contour(X, Y, self.sources.potential(), levels=[-1,0,1],extend='both',linestyles='dashed',linewidths=2,colors='#000000')
        cbar = plt.colorbar(contf)
        cbar.set_label('$\Phi$', fontsize=fsize)
        #cbar.set_ticks([int(minPot), -1.0, 0.0, 1.0])

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

        contf = plt.contourf(X, Y, self.sources.getCp(), levels=np.linspace(-2.0, 1.2, 100), extend='both')
        trash = plt.contour(X, Y, self.sources.getCp(), levels=[0.90], colors='#000000', linewidths=2, linestyles='dashed')
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')
        cbar = plt.colorbar(contf)
        cbar.set_label('$C_p$', fontsize=fsize)
        cbar.set_ticks([-2.0, -1.0, 0.0, 1.0])

    def plotBody(self, line='solid'):
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        plt.contour(X, Y, self.sources.streamFunction(), levels= [0.0], colors='#CD2305', linewidths=2, linestyles=line)


def f2m(l):
    return l*0.3048
def m2f(m):
    return m/0.3048

if __name__ == '__main__':

    ## Settings for Shaffers long body
    u_inf = f2m(10)                 # 10 feet/s    Shaffer page 13
    x_offset = f2m(4.18)            # 4.18 ft from Shaffer page 5
    y_offset = 0.0
    clDepth      = f2m(3)           # 3 feet    Shaffer page 13
    sourceFactor = 0.104            # From page 5 in Shaffer ( 4*pi ??)

    ## Settings for Shaffers short body
    #x_offset = f2m(2.09)            # 4.18 ft from Shaffer page 5
    #y_offset = 0.0
    #clDepth      = f2m(1.5)         # 3 feet    Shaffer page 13
    #sourceFactor = 0.026            # From page 5 in Shaffer ( 4*pi ??)

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

    plt.show()

    # -Rankine Body ----------------------------------
    body = rankineBody(Sources,clDepth)

    if body.ok():
        wl =  body.getWaveLength()

        body.solveDimensions(guess=1.0)
        body.info()

        plt.figure(figsize=figureSize)
        downstreamCoordinates = np.linspace(x_offset*2,8*wl,400)
        wh = body.plotWaves(downstreamCoordinates)
        print 'Max wave h  = {0:8.2f} m, {1:8.2f} inch'.format(max(wh),m2f(max(wh)*12))
        print 'Wave length = ',wl
        plt.show()
    # ------------------------------------------------

