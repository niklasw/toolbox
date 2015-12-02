#!/usr/bin/python
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi

x = np.arange(0,4*pi,0.01)
y = np.sin(x)
z = np.cos(y)

xTickLoc = np.arange(0,x.max()+1,pi)

tickLabels = [ '{0:0.0f} $\pi$'.format(a) for a in xTickLoc/pi ]

plt.xticks(xTickLoc, tickLabels, rotation=35)

plt.grid('on')

plt.plot(x,y,linewidth=2,color='red',linestyle='--')
plt.plot(x,z,linewidth=2,color='green',linestyle='-')

plt.show()



