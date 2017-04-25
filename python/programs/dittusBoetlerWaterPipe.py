#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 22}

matplotlib.rc('font', **font)

M=np.linspace(0.1,1,100)
D=0.01;

rho=1000.0
nu=1e-6
Pr=3.5
k=0.58 # Thermal conductivity water

r=0.5*D
A=math.pi*r**2
U=M/(rho*A)
Re=U*D/nu

def Nusselt(Re,Pr,n=0.4):
    # Dittus-Boelter approximation.
    # n=0.4 for heating of flow, 0.3 for cooling
    return 0.023*pow(Re,4.0/5.0)*Pr**n

def HTC(Nusselt,Di,k, setFix=-1.0):
    if setFix < 0:
        return Nusselt*k/Di
    else:
        return setFix

fig,ax1 = plt.subplots(figsize=(14,9))
ax2 = ax1.twinx()

ax1.plot(M,HTC(Nusselt(Re,Pr),D,k),label='HTC',linewidth=2)
ax1.set_ylabel('HTC [W/m$^2$K]',color='b')

ax2.plot(M,U,color='r',label='Bulk velocity',linewidth=2)
ax2.set_ylabel('Bulk velocity [m/s]',color='r')

plt.title('Water pipe, diameter = {0:0.0f} mm'.format(D*1000))
ax1.grid('on')
ax1.set_xlabel('Mass flow [kg/s]')
plt.savefig('pipeHtc.png')
plt.show()

