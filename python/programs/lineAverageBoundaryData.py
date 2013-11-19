#!/usr/bin/python
import sys
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from matplotlib import cm

X_scale=1.3
dataFile = sys.argv[1]#'export_splitFlux.csv'
outDataFile = 'Carton_surface_averaged.csv'

surfaceData = loadtxt(dataFile,skiprows=6,delimiter=',')

Ytmp=surfaceData[:,1]
Ymin = -0.0222
relevantItems = where(Ytmp>Ymin)[0]

X  = surfaceData[:,0][relevantItems]
Z  = surfaceData[:,2][relevantItems]/X_scale
T  = surfaceData[:,3][relevantItems]
htc= surfaceData[:,4][relevantItems]

Small = 1e-11
newGrid = {'X':50,'Z':200}

print "Number of data points =", X.size
print "Problem size = ", X.size*newGrid['X']*newGrid['Z']


x_cart = linspace(X.min(),X.max(),newGrid['X'])
z_cart = linspace(Z.min(),Z.max(),newGrid['Z'])

interp_htc        = arange(x_cart.size*z_cart.size)
interp_T          = arange(x_cart.size*z_cart.size)
interp_htc.shape  = x_cart.size,z_cart.size
interp_T.shape    = x_cart.size,z_cart.size

def ShepardInterpolate2d(x,y,X,Y,u,p=2):
    distX = X-x
    distY = Y-y
    d = sqrt(distX**2.0+distY**2.0)
    w=1.0/(d**p+Small)
    return sum(w*u/sum(w))

for k,z in enumerate(z_cart):
    for i,x in enumerate(x_cart):
        interp_T[i,k] = ShepardInterpolate2d(x,z,X,Z,T,3.0)
        interp_htc[i,k] = ShepardInterpolate2d(x,z,X,Z,htc,3.0)

print interp_htc.size, x_cart.size,z_cart.size

print 'Min original values = ', htc.min(), T.min()
print 'Max original values = ', htc.max(), T.max()
print 'Min interpolated values = ', interp_htc.min(), interp_T.min()
print 'Max interpolated values = ', interp_htc.max(), interp_T.max()

fig=figure(1,figsize=(10,20))
nConts = 55

subplot(611)
contourf(z_cart,x_cart,interp_htc,nConts,cmap=cm.jet)
axis('equal')
title('Interpolated HTC')
xlabel('z')
ylabel('x')
grid('on')

subplot(612)
contourf(z_cart,x_cart,interp_T,nConts,cmap=cm.jet)
axis('equal')
title('Interpolated T')
xlabel('z')
ylabel('x')
grid('on')



averagedHtc=average(interp_htc,axis=0)
averagedT=average(interp_T,axis=0)

for i,h in enumerate(z_cart):
    interp_htc[:,i] = averagedHtc[i]
    interp_T[:,i] = averagedT[i]


fo = file(outDataFile,'w')

header= """
[Name]
Cartonsurface

[Spatial Fields]
x,y,z

[Data]
x [ m ], y [ m ], z [ m ], Wall Adjacent Temperature [ K ], Wall Heat Transfer Coefficient [ W m^-2 K^-1 ]
"""

fo.write(header)
for k,z in enumerate(z_cart):
    for i,x in enumerate(x_cart):
        fo.write('%f, %f, %f, %f, %f\n' % (x,Ymin,z,interp_T[i,k],interp_htc[i,k]))

subplot(613)
contourf(z_cart,x_cart,interp_htc,nConts,cmap=cm.jet)
axis('equal')
title('X-averaged HTC')
xlabel('z')
ylabel('x')
grid('on')

subplot(614)
contourf(z_cart,x_cart,interp_T,nConts,cmap=cm.jet)
axis('equal')
title('X-averaged T')
xlabel('z')
ylabel('x')
grid('on')

subplot(615)
plot(z_cart,averagedHtc)
title('X-averaged HTC')
xlabel('z')
ylabel('HTC')
grid('on')

subplot(616)
plot(z_cart,averagedT)
title('X-averaged T')
xlabel('z')
ylabel('T')
grid('on')


savefig('lineAverageBoundaryData.png')

show()

