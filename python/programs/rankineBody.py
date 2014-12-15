#!/usr/bin/python

from math import *
import numpy as np
import matplotlib.pyplot as plt


N = 200                               # Number of points in each direction
x_start, x_end = -40.0, 40.0            # x-direction boundaries
y_start, y_end = -20.0, 20.0            # y-direction boundaries
x = np.linspace(x_start, x_end, N)    # 1D-array for x
y = np.linspace(y_start, y_end, N)    # 1D-array for y
X, Y = np.meshgrid(x, y)              # generates a mesh grid

u_inf = 1.0        # freestream speed

# computes the freestream velocity field
u_freestream = u_inf * np.ones((N, N), dtype=float)
v_freestream = np.zeros((N, N), dtype=float)

# computes the stream-function
psi_freestream = u_inf * Y

def get_velocity(strength, xs, ys, X, Y):
    """Returns the velocity field generated by a source/sink.

    Arguments
    ---------
    strength -- strength of the source/sink.
    xs, ys -- coordinates of the source/sink.
    X, Y -- mesh grid.
    """
    u = strength/(2*pi)*(X-xs)/((X-xs)**2+(Y-ys)**2)
    v = strength/(2*pi)*(Y-ys)/((X-xs)**2+(Y-ys)**2)

    return u, v

def get_stream_function(strength, xs, ys, X, Y):
    """Returns the strem-function generated by a source/sink.

    Arguments
    ---------
    strength -- strength of the source/sink.
    xs, ys -- coordinates of the source/sink.
    X, Y -- mesh grid.
    """
    psi = strength/(2*pi)*np.arctan2((Y-ys), (X-xs))

    return psi

def get_waves(strength, depth, U, distance):
    """Returns steady-state waves resulting from rankine body"""
    # Adhere to the report terminology:
    M = float(strength)
    f = float(depth)
    R = float(distance)


    g = 9.81
    h = 4*M/U*np.sqrt(2*np.pi*g/(R*U**2))*exp((-g*f)/U**2)*cos(g*R/U**2+np.pi/4)


strength_source = 10.0            # strength of the source
x_source, y_source = -25.0, 0.0   # location of the source

strength_sink = -strength_source        # strength of the sink
x_sink, y_sink = 25.0, 0.0   # location of the sink

# computes the stream-function
psi_source = get_stream_function(strength_source, x_source, y_source, X, Y)
psi_sink = get_stream_function(strength_sink, x_sink, y_sink, X, Y)

u_source, v_source = get_velocity(strength_source, x_source, y_source, X, Y)
u_sink, v_sink = get_velocity(strength_sink, x_sink, y_sink, X, Y)


# superposition of a source and a sink on the freestream
u = u_freestream + u_source + u_sink
v = v_freestream + v_source + v_sink
psi = psi_freestream + psi_source + psi_sink

# plots the streamlines
#%matplotlib inline

size = 10
plt.figure(figsize=(size, (y_end-y_start)/(x_end-x_start)*size))
plt.grid(True)
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.streamplot(X, Y, u, v, density=2, linewidth=1, arrowsize=1, arrowstyle='->')
plt.scatter([x_source, x_sink], [y_source, y_sink], color='#CD2305', s=80, marker='o')

# calculates the stagnation point
x_stagnation = x_source - strength_source/(2*pi*u_inf)
y_stagnation = y_source

# adding the stagnation point to the figure
plt.scatter(x_stagnation, y_stagnation, color='g', s=80, marker='o')

# adds the dividing line to the figure
plt.contour(X, Y, psi,
            levels=[0.],
            colors='#CD2305', linewidths=2, linestyles='solid');


# computes the pressure coefficient field
cp = 1.0 - (u**2+v**2)/u_inf**2

# plots the pressure coefficient field
plt.figure(figsize=(1.1*size, (y_end-y_start)/(x_end-x_start)*size))
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
contf = plt.contourf(X, Y, cp, levels=np.linspace(-2.0, 1.0, 100), extend='both')
cbar = plt.colorbar(contf)
cbar.set_label('$C_p$', fontsize=16)
cbar.set_ticks([-2.0, -1.0, 0.0, 1.0])
plt.scatter([x_source, x_sink], [y_source, y_sink], color='#CD2305', s=80, marker='o')
plt.contour(X, Y, psi, levels=[0.], colors='#CD2305', linewidths=2, linestyles='solid');

plt.show()


