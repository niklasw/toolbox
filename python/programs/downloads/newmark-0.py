#!/usr/bin/python

'''
Program solves the wave equation
 
  u_tt -(cu_x)_x= f    on [0,1]
  u(0, t)= u0
  u(1, t)= u1
  u(x,0) = u_init

using Newmark's method
'''
#----------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Animation.FuncAnimation makes an animation 
# by repeatedly calling a function compute_time_step 
# (where all the calculation is done), passing in arguments in data_time

#----------------------------------------------------------

# Set space discretization parameters
n = 150 # number of inner points
dx, x = 1./(n+1), np.linspace(0.0, 1.0, n+2)

# Set space discretization parameters
t, dt, T = 0.0, 0.01, 10.
beta = 0.4
gamma = 0.6

def time_gen():
    global t
    t = 0.0
    while t < T:
        t += dt
        yield t

#----------------------------------------------------------  
  
# Newmark's method parameters
gamma = .5
beta = .25

#----------------------------------------------------------


# Define the discretizated source f and diffusion coefficient c 
c = 0.1
f = 0.0

# Set boundary conditions
u0 = 1.0
u1 = 1.0

# Set initial conditions
p = np.cos(2.*np.pi*x)
q = x*0.0

#----------------------------------------------------------

# Assemble the Poisson supbroblem
D =  np.hstack((np.diag(-np.ones(n+1)), np.zeros((n+1,1)))) + np.hstack((np.zeros((n+1,1)),np.diag(np.ones(n+1))))
L = np.dot(D.T, c*D)/(dx**2.) # L = -D^-*c*(D^+)
L[0,1], L[-1,-2] = 0., 0. # Dirichlet BC

# Assemble the right side for the Poisson supbroblem
b_s = np.zeros(n+2)
b_s[0], b_s[-1] = c*u0/(dx**2.), c*u1/(dx**2.) 
b_s[1:-1] += f 

# Array of unknowns r = [u, v, z]^T
z = b_s -np.dot(L, p)
r_0 = np.hstack((p, q, z))
r_ = np.array(r_0)

# Compose the system matrix
I = np.eye(n+2)
O = np.zeros((n+2,n+2))
A = np.bmat([[L, O, I], [O, I, -dt*gamma*I], [I, O, -dt**2.*beta*I]])

# Dummy right side
b = np.empty_like(r_)

#----------------------------------------------------------

# Set up the plots
fig, ax = plt.subplots()
ax.set_ylim(-2., 4.0)
ax.set_xlim(0., 1.)
ax.grid()
time_template = 'Time = %.5f s'    # prints running simulation time
time_text = ax.text(0.8, 0.95, '', transform=ax.transAxes)
line, = ax.plot(x, r_[:n+2], lw=2)

#----------------------------------------------------------

# Computes the solution at a time step and returns its graph
def compute_time_step(t, r_, r_0):
    # Compute new step
    new_t = t
    # Feed the right side
    b[:n+2] = -b_s[:]
    b[n+2:2*(n+2)] = r_0[n+2:2*(n+2)] + dt*(1.-gamma)*r_0[2*(n+2):]
    b[2*(n+2):] = r_0[:n+2] + dt*r_0[n+2:2*(n+2)]  + 0.5*dt**2.*(1.-2.*beta)*r_0[2*(n+2):]
    
    # Compute solution and update
    r_[:] = np.linalg.solve(A,b)[:]
    r_0[:] = r_[:]
    line.set_ydata(r_[:n+2])
    time_text.set_text(time_template%(t))
    return line, time_text,

def init():
    # just for blank backround
    line.set_ydata(np.ma.array(x, mask=True)) 
    return line,
  
ani = animation.FuncAnimation(fig, compute_time_step, time_gen, fargs = (r_, r_0), init_func=init, blit=True, interval=100, repeat=True)
plt.show()

