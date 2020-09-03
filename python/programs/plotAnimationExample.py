#!/usr/bin/env python3

from matplotlib import animation
from matplotlib import pyplot as plt
import numpy as np
PI = np.pi

fig,ax = plt.subplots()
line, = plt.plot([],[],linewidth=2)
plt.grid('on')

nFrames = 48 
iFrames = np.arange(nFrames)

xcoord = np.linspace(0,4*PI,1000)

ax.set_xlim(0,4*PI)
ax.set_ylim(-1.1,1.1)

#def initLine():
#    line.set_data([],[])
#    ax.set_xlim(0,4*PI)
#    ax.set_ylim(-1.1,1.1)
#    return line,

def updateLine(t):
    line.set_data(xcoord,np.sin(xcoord*0.1*t))
    return line,

anim = animation.FuncAnimation(fig,updateLine, \
                                   frames=iFrames, \
                                   blit=True)

#plt.show()
anim.save('filename.mp4',fps=24)



