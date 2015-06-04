#!/usr/bin/python

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
        plt.xlabel('$x$', fontsize=self.fsize)
        plt.ylabel('$y$', fontsize=self.fsize)
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
        '''Velocity from numerical gradient of potential'''
        dx, dy = self.mesh.deltas
        u,v = np.gradient(self.potential(),dx,dy)
        return (v,u) # reversed, due to indexing...

    def streamFunction(self):
        return self.strength*(1-self.X/(4*pi*self.r))

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
        #return self.mesh.Y*self.u
        return 0.5*self.u*self.mesh.Y**2

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

    def strengths(self):
        return np.array([S.strength for S in self])

def solveSources(U, length, aspect):
    l = length/2
    h = aspect*l

    Z    = np.pi*U*h**2
    diff = 1.0
    eps = 1e-8
    #- Initial M guess
    M = Z*1.1

    while diff > eps:
        #- Compute c(M) from eq3 Shaffer
        A = Z/M
        c = A*h/sqrt(1-A*A)

        #- Newton-Rapson find root for eq2
        X = l*l-c*c
        Y = l/(np.pi*U)

        f = X*X - c*M*Y

        dAdM = -A/M
        dcdM = dAdM*c*(1/A + A/(1-A*A))
        dXdM = -2*c*dcdM;
        dfdM = 2*X*dXdM - (dcdM*M + c)*Y;

        delM = f/dfdM
        M-=delM
        diff = np.abs(delM)
        print 'looping'
        if M < Z:
            print 'M corrected'
            M = 1.01*Z

    A = Z/M
    c = A*h/sqrt(1-A*A)

    return c,M

class rankine:
    def __init__(self,length,aspect,freestream,depth,g=9.81):
        self.fs = freestream
        self.depth = depth
        self.g = g
        self.length = length
        self.aspect = aspect
        self.width = length*aspect
        self.sources = sourceList(freestream.mesh)
        self.sources.fs = freestream
        self.offset = (0.0,0.0)
        self.solveSources()

    def ok(self):
        '''Just a method to turn of rankine body calculations
        if not all parameters are available, e.g. lacking
        freestream'''
        return ((len(self.sources) == 2) and (self.fs.u != 0))

    def solveSources(self):
        l = self.length/2.0
        h = self.aspect*l
        U = self.fs.u

        Z    = np.pi*U*h**2
        diff = 1.0
        eps = 1e-8
        #- Initial M guess
        M = Z*1.1

        while diff > eps:
            #- Compute c(M) from eq3 Shaffer
            A = Z/M
            c = A*h/sqrt(1-A*A)

            #- Newton-Rapson find root for eq2
            X = l*l-c*c
            Y = l/(np.pi*U)

            f = X*X - c*M*Y

            dAdM = -A/M
            dcdM = dAdM*c*(1/A + A/(1-A*A))
            dXdM = -2*c*dcdM;
            dfdM = 2*X*dXdM - (dcdM*M + c)*Y;

            delM = f/dfdM
            M-=delM
            diff = np.abs(delM)
            if M < Z:
                M = 1.01*Z

        A = Z/M
        c = A*h/sqrt(1-A*A)

        self.sources.addSource( M,-c+self.offset[0],self.offset[1])
        self.sources.addSource(-M, c+self.offset[0],self.offset[1])

        print "c, M =", c,M

        return c,M

    def Froude(self,L):
        g = self.g
        U = sqrt(self.fs.u**2+self.fs.v**2)
        Fr =  U/sqrt(g*L)
        return U/sqrt(g*L)

    def waves(self,distance):
        '''Superposition of waves from all sources
        '''
        wh = np.zeros(len(distance))
        for S in self.sources:
            wh += self.singleSourceWaves(distance,S)
        return wh/(4*pi)

    def singleSourceWaves(self,distance,source):
        '''Wave pattern from a single source moving beneath
        a free surface  according to Shaffer/Yim'''
        M = source.strength
        f = abs(self.depth)
        c = source.x
        cSign = c/abs(c)
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

    def writeWaves(self,distance):
        wh = self.waves(distance)

        with open('RankineBodyWaves.dat','w') as fp:
            fp.write('# X elevation\n')
            for i,d in enumerate(distance):
                w = wh[i]
                fp.write('{0} {1}\n'.format(d,w))


    def info(self):
        def m2f(m):
            return m/0.3048
        c = abs(self.sources[0].x)
        print 'Velocity    = {0:8.2f} m/s, {1:8.2f} f/s'.format(self.fs.u,m2f(self.fs.u))
        print 'Src offset  = {0:8.2f} m, {1:8.2f} f'.format(c,m2f(c))
        print 'Body Lpp    = {0:8.2f} m, {1:8.2f} feet'.format(self.length,m2f(self.length))
        print 'Body w      = {0:8.2f} m, {1:8.2} feet'.format(self.width,m2f(self.width))
        print 'Body aspect = {0:8.2f}'.format(self.length/self.width)
        print 'Cl depth    = {0:8.2f} m, {1:8.2f} feet'.format(self.depth,m2f(self.depth))
        print 'Froude(d)   = {0:8.2f}'.format(self.Froude(self.depth))



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
            print 'WARNING: cannot solveDimensions. U=0!'
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

            print "WARNING: Solver did not converge!"
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

    def waves(self,distance):
        '''Superposition of waves from all sources
        '''
        wh = np.zeros(len(distance))
        for S in self.sources:
            wh += self.singleSourceWaves(distance,S)
        return wh/(4*pi)

    def singleSourceWaves(self,distance,source):
        '''Wave pattern from a single source moving beneath
        a free surface  according to Shaffer/Yim'''
        M = source.strength
        f = abs(self.depth)
        c = source.x
        cSign = c/abs(c)
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

    def writeWaves(self,distance):
        wh = self.waves(distance)

        with open('RankineBodyWaves.dat','w') as fp:
            fp.write('# X elevation\n')
            for i,d in enumerate(distance):
                w = wh[i]
                fp.write('{0} {1}\n'.format(d,w))


    def info(self):
        def m2f(m):
            return m/0.3048
        c = abs(self.sources[0].x)
        print 'Velocity    = {0:8.2f} m/s, {1:8.2f} f/s'.format(self.fs.u,m2f(self.fs.u))
        print 'Src offset  = {0:8.2f} m, {1:8.2f} f'.format(c,m2f(c))
        print 'Body Lpp    = {0:8.2f} m, {1:8.2f} feet'.format(self.length,m2f(self.length))
        print 'Body w      = {0:8.2f} m, {1:8.2} feet'.format(self.width,m2f(self.width))
        print 'Body aspect = {0:8.2f}'.format(self.length/self.width)
        print 'Cl depth    = {0:8.2f} m, {1:8.2f} feet'.format(self.depth,m2f(self.depth))
        print 'Froude(d)   = {0:8.2f}'.format(self.Froude(self.depth))

class canvas:
    '''Object to handle all the plotting'''

    def __init__(self,sources):
        self.sources = sources
        self.fsize = 24
        self.lblsize = 15

    def new(self, size):
        plt.figure(figsize=size)
        plt.tick_params(axis='both', which='both', labelsize=self.lblsize)

    def sub(self,nnn=111):
        plt.subplot(nnn)
        plt.tick_params(axis='both', which='both', labelsize=self.lblsize)


    def decorate(self,title='',ylabel='$y$',xlabel='$x$'):
        if title:
            plt.title(title,fontsize=self.fsize)
        plt.grid(True)
        plt.xlabel(xlabel, fontsize=self.fsize*1.5)
        plt.ylabel(ylabel, fontsize=self.fsize*1.5)

    def present(self,figName):
        plt.tight_layout()
        plt.savefig(figName)
        plt.show()

    def plotStreamlines(self):
        self.decorate()
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        u,v = self.sources.velocity()
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        plt.streamplot(X, Y, u, v, density=2, color='#888888', linewidth=1, arrowsize=1, arrowstyle='->')
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

    def plotStreamfunction(self):
        self.decorate('Streamfunction')
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        u,v = self.sources.velocity()
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        strf = self.sources.streamFunction()

        contf = plt.contourf(X, Y, strf, levels=np.linspace(strf.min(),strf.max(),50),extend='both',cmap=plt.cm.RdBu_r)
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

        cbarTicks = np.arange(0,strf.max(),0.5)
        print cbarTicks
        cbar = plt.colorbar(contf,ticks=cbarTicks)
        cbar.set_label('$\Psi$', fontsize=self.fsize)
        plt.axis('equal')

    def plotPotential(self):
        self.decorate('Potential')
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        pot = self.sources.potential()
        maxPot = pot.max()*0.5
        minPot = pot.min()*0.5

        contf = plt.contourf(X, Y, self.sources.potential(), levels=np.linspace(minPot,maxPot,50), extend='both',cmap=plt.cm.RdBu_r)
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

        cbarTicks = [int(a) for a in np.arange(minPot,maxPot,2.0)]
        cbar = plt.colorbar(contf, ticks=cbarTicks)
        cbar.set_label('$\Phi$', fontsize=self.fsize)
        plt.axis('equal')

    def plotCp(self):
        self.decorate('Pressure coefficient, $C_p$')
        plt.grid(True)
        plt.xlabel('$x$', fontsize=self.fsize*1.5)
        plt.ylabel('$y$', fontsize=self.fsize*1.5)
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        x_sources = [s.x for s in self.sources]
        y_sources = [s.y for s in self.sources]

        contf = plt.contourf(X, Y, self.sources.getCp(), levels=np.linspace(-0.5, 1.0, 50), extend='both',cmap=plt.cm.RdBu_r)
        trash = plt.contour(X, Y, self.sources.getCp(), levels=[0.90], colors='#000000', linewidths=2, linestyles='dashed')
        #plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')

        cbar = plt.colorbar(contf)
        cbar.set_label('$C_p$', fontsize=self.fsize)
        cbar.set_ticks([-0.5, 0.0, 0.5, 1.0])
        plt.axis('equal')

    def plotBody(self, line='solid', color='#CD2305'):
        X = self.sources.mesh.X
        Y = self.sources.mesh.Y
        L = [0]
        contf = plt.contour(X, Y, self.sources.streamFunction(), levels=L, colors=color, linewidths=2, linestyles=line)
        return contf

    def plotBodyAndSaveGeometry(self, line='solid', color='#CD2305',fileName='body'):
        '''Plots the streamfunction value 0 iso-contour AND extracts the
        plot point coordinates. The extracted coordinates are saved in wavefront
        .obj format, since it can be imported by e.g. Blender and Paraview.'''
        contf = self.plotBody(line,color)

        #- Extract and save body contour as geometry file
        path = contf.collections[0].get_paths()[0]
        vertices = path.vertices
        with open(fileName+'.obj','w') as obj:
            X = zip(vertices[:,0], vertices[:,1])
            print X[0]
            print X[1]
            obj.write('o {0}_mesh\n'.format(fileName))
            for v in X:
                obj.write('v {0} {1} 0\n'.format(v[0],v[1]))
            for i in range(1,len(X)):
                obj.write('l {0} {1}\n'.format(i,i+1))

        #- Extract and report body size
        L = vertices[:,0].max() - vertices[:,0].min()
        W = vertices[:,1].max() - vertices[:,1].min()
        print '\nBody dimensions, extracted from body plot:'
        print '\tplotBody L    = {0:8.2f} m'.format(L)
        print '\tplotBody W    = {0:8.2f} m\n'.format(W)

    def plotWaves(self,body,distance, normalize=False):
        wh = body.waves(distance)

        if normalize:
            wh *= body.fs.u*body.depth/abs(body.sources[0].strength)
            distance /= body.length

        plt.plot(distance,wh,'#053061',linewidth=2)
        #plt.plot(distance-1.36,wh2,'g')

        self.decorate('Waves @ $C_L$',ylabel='$\zeta$')
        plt.grid('on')
        plt.xlim(-2,np.max(distance))
        #plt.ylim(-2*np.max(wh[len(wh)/2:]),2*np.max(wh[len(wh)/2:]))

        x_sources = [s.x for s in body.sources]
        y_sources = [s.y for s in body.sources]
        plt.scatter(x_sources, y_sources, color='#CD2305', s=80, marker='o')




