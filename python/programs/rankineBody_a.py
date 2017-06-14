#!/usr/bin/python

import sys
from potentialFlow import mesh,source,freeStream,sourceList,rankine,canvas
from matplotlib import pyplot as plt
import numpy as np

def f2m(l):
    return l*0.3048
def m2f(m):
    return m/0.3048

if __name__ == '__main__':

    ## Settings for Shaffers 9 ft 7/1 body
    u_inf = f2m(10)                 # 10 feet/s    Shaffer page 13
    clDepth  = f2m(3)               # 3 feet    Shaffer page 13

    L = f2m(9)
    aspect = 1.0/7

    Mesh = mesh(-L,L,-L/2,L/2,1200,800)

    fs = freeStream(u_inf,0.0,Mesh)

    pos0 = (.0,.0)
    body = rankine(L,aspect,pos0,fs,clDepth)

    body.info()
    wl =  body.getWaveLength()

    size = 15
    figureSize = (size, (Mesh.dimensions()[1])/(Mesh.dimensions()[0])*size)

    c = canvas(body.sources)
    c.new(figureSize)
    c.plotPotentialFlow()

    # -Rankine Body ----------------------------------
    sourceOffset = abs(body.sources[0].x)
    downstreamCoordinates = np.linspace(sourceOffset*2,8*wl,400)
    c.sub(224)
    c.plotWaves(body,downstreamCoordinates, normalize=False)
    #body.writeWaves(downstreamCoordinates)
    # ------------------------------------------------
    c.present('RankineBodyWaves.png')

