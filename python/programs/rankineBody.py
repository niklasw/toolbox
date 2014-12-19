#!/usr/bin/python
# Ripped parts from
# http://nbviewer.ipython.org/github/barbagroup/AeroPython/blob/master/lessons/02_Lesson02_sourceSinkFreestream.ipynb


from math import *
import numpy as np
import matplotlib.pyplot as plt


def R(x0,y0,X,Y):
    return np.sqrt((Y-y0)**2+ (X-x0)**2)

def get_velocity_3d(strength, x0, y0, X, Y):
    """Returns the velocity field generated by a source/sink.

    Arguments
    ---------
    strength -- strength of the source/sink.
    x0, y0 -- coordinates of the source/sink.
    X, Y -- mesh grid.
    """
    r = R(x0,y0,X,Y)

    u = strength/(4*pi) * (X-x0)/(4*pi*r**3)
    v = strength/(4*pi) * (Y-y0)/(4*pi*r**3)

    return u, v

def get_potential_3d(strength, x0, y0, X, Y):
    """Returns the potential generated by one source/sink.

    Arguments
    ---------
    strength -- strength of the source/sink.
    x0, y0 -- coordinates of the source/sink.
    X, Y -- mesh grid.
    At Z == 0
    """
    r = R(x0,y0,X,Y)

    phi = strength/(4*pi*r)

    return phi

def get_stream_function_3d(strength, x0, y0, X, Y):
    """Returns the strem function generated by one source/sink.

    Arguments
    ---------
    strength -- strength of the source/sink.
    x0, y0 -- coordinates of the source/sink.
    X, Y -- mesh grid.
    At Z == 0
    """
    r = R(x0,y0,X,Y)

    psi = strength/(4*pi)*(1.0-(X-x0)/(4*pi*r))

    return psi

def getWaveLength(U,g=9.81):
    """Wave length according to Shaffer/Yim"""
    return 2*pi*U**2/g

def Froude(U,L,g=9.81):
    """Froude number"""
    return U/sqrt(L*g)


def rankine_waves(strength, depth, U, source_x, distance, g=9.81):
    """Center line wave shape from a sink and a source, forming a Rankine body"""
    M = float(strength)/(4*pi)
    f = float(depth)
    c = float(source_x)

    Fr = Froude(U,f,g)            # Froud number of depth
    B = 8*M/(f**2*U*Fr) * exp(-1/Fr**2) * sin(c/(f*Fr**2))
    h2f = lambda R: B*sqrt(2*pi*f/R) * sin(R/(f*Fr**2) - 3*pi/4)

    return [f*h2f(R) for R in distance ]

def getSourceFromStagnation(x,U,c):
    """Verification only"""
    M = (x**2-abs(c)**2)**2/(x*c)*pi*U
    M*=4*pi
    print "\tSource strength validation M = {0}".format(M)

    return M

def solveDimensions(strength, U, source_x, guess):
    c=abs(source_x)
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
    
def feet(l):
    return l*0.3048

# Problem setup

g = 9.81
depthFactor = 4                 # Operating depth = beam*depthFactor
strengthFactor = 0.1
u_inf = 1.5                      # freestream speed
strength_source = u_inf*strengthFactor*4*pi     # strength of the source/sink
strength_sink = -strength_source # strength of the sink
x_source, y_source = -1.4, 0.0    # location of the source
x_sink, y_sink = -x_source, 0.0  # location of the sink

# Mesh generation
N = 500                               # Number of points in each direction
x_start, x_end = 2*x_source, -2*x_source            # x-direction boundaries
y_start, y_end = 1*x_source, -1*x_source            # y-direction boundaries
x = np.linspace(x_start, x_end, N)    # 1D-array for x
y = np.linspace(y_start, y_end, N)    # 1D-array for y
X, Y = np.meshgrid(x, y)              # generates a mesh grid


# computes the stream-function
psi_freestream = 0.5*u_inf*Y**2
psi_source = get_stream_function_3d(strength_source, x_source, y_source, X, Y)
psi_sink   = get_stream_function_3d(strength_sink, x_sink, y_sink, X, Y)

# computes the freestream velocity field
u_freestream = u_inf * np.ones((N, N), dtype=float)
v_freestream = np.zeros((N, N), dtype=float)

u_source, v_source = get_velocity_3d(strength_source, x_source, y_source, X, Y)
u_sink, v_sink     = get_velocity_3d(strength_sink, x_sink, y_sink, X, Y)

pot_freestream = u_inf*X
pot_source = get_potential_3d(strength_source, x_source, y_source, X, Y)
pot_sink   = get_potential_3d(strength_sink, x_sink, y_sink, X, Y)


# superposition of a source and a sink on the freestream
u = u_freestream + u_source + u_sink
v = v_freestream + v_source + v_sink
psi = psi_freestream + psi_source + psi_sink
pot =  pot_freestream + pot_source + pot_sink

# plots the streamlines
size = 10
figureSize = (size, (y_end-y_start)/(x_end-x_start)*size)

plt.figure(figsize=figureSize)
plt.grid(True)
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.streamplot(X, Y, u, v, density=3, linewidth=1, arrowsize=2, arrowstyle='->')
plt.scatter([x_source, x_sink], [y_source, y_sink], color='#CD2305', s=80, marker='o')

# adds the dividing line to the figure
contf=plt.contour(X, Y, psi,
            levels= [0],
            colors='#CD2305', linewidths=2, linestyles='solid')

# computes the presnsure coefficient field
cp = 1.0 - (u**2+v**2)/u_inf**2

# plots the pressure coefficient field
plt.figure(figsize=figureSize)
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
contf = plt.contourf(X, Y, cp, levels=np.linspace(-2.0, 1.0, 100), extend='both')
cbar = plt.colorbar(contf)
cbar.set_label('$C_p$', fontsize=16)
cbar.set_ticks([-2.0, -1.0, 0.0, 1.0])
plt.scatter([x_source, x_sink], [y_source, y_sink], color='#CD2305', s=80, marker='o')
plt.contour(X, Y, psi, levels=[0.], colors='#CD2305', linewidths=2, linestyles='dashed');

print "Source strength input = {0}".format(strength_source)
print "Source pair distance  = {0}".format(2*abs(x_source))

# stationary wave generation according to Yim/Shaffer

lpp,beam = solveDimensions(strength_source, u_inf, x_source, guess=0.5)
operatingDepth = beam*depthFactor
waveLength = getWaveLength(u_inf,g)
maxLength = 10*waveLength
getSourceFromStagnation(lpp/2,u_inf,x_sink)
print "Wave length = {0}".format(waveLength)
print "Depth Froude number = {0}".format(Froude(u_inf,operatingDepth))
print "Froude number (Lpp) = {0}".format(Froude(u_inf,lpp))
print "Length, beam and aspect = {0}, {1}, {2}".format(lpp,beam,lpp/beam)
print "Operating depth = {0}".format(operatingDepth)

distance = np.arange(0.1,maxLength,0.01)

# Calculate and plot waves
wh = rankine_waves(strength_source, operatingDepth, u_inf, x_source, distance)
plt.figure()
plt.xlabel('Distance')
plt.ylabel('Centerline surface elevation')
plt.plot(distance,wh)
plt.grid('on')
plt.xlim(0,maxLength)
plt.ylim(-1.1*np.max(wh),1.1*np.max(wh))

plt.show()

