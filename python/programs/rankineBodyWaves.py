#!/usr/bin/python

import sys
from potentialFlow import mesh,source,freeStream,sourceList,rankineBody,canvas
from matplotlib import pyplot as plt
import numpy as np

def f2m(l):
    return l*0.3048
def m2f(m):
    return m/0.3048

if __name__ == '__main__':

    ## Settings for Shaffers 9 ft 7/1 body
    u_inf = f2m(10)                 # 10 feet/s    Shaffer page 13
    x_offset = f2m(4.18)            # 4.18 ft from Shaffer page 5
    y_offset = 0.0
    clDepth      = f2m(3)           # 3 feet    Shaffer page 13
    sourceFactor = 0.104            # From page 5 in Shaffer ( 4*pi ??)

    ## Settings for Shaffers 4.5 ft 7/1 body
    #x_offset = f2m(2.09)            # 4.18 ft from Shaffer page 5
    #y_offset = 0.0
    #clDepth      = f2m(1.5)         # 3 feet    Shaffer page 13
    #sourceFactor = 0.026            # From page 5 in Shaffer ( 4*pi ??)

    sourceStrength = u_inf * sourceFactor

    Mesh = mesh(-1.5*x_offset,1.5*x_offset,-1*x_offset, 1*x_offset,600,400)

    Sources = sourceList(Mesh)
    Sources.addSource( sourceStrength, -x_offset, y_offset)
    Sources.addSource(-sourceStrength,  x_offset, y_offset)
    Sources.addFreeStream(u_inf,0)

    body = rankineBody(Sources,clDepth)

    size = 15
    figureSize = (size, (Mesh.dimensions()[1])/(Mesh.dimensions()[0])*size)

    c = canvas(Sources)

    c.new(figureSize)

    c.sub(221)
    c.plotStreamlines()
    c.plotStreamfunction()
    if body.ok():
        c.plotBodyAndSaveGeometry(line='solid', color='#ffffff',fileName='RankineBody')
    else:
        c.plotBody(line='solid', color='#ffffff')

    c.sub(222)
    c.plotPotential()
    c.plotBody(line='solid', color='#000000')

    c.sub(223)
    c.plotCp()
    c.plotBody(line='solid', color='#000000')



    # -Rankine Body ----------------------------------
    if body.ok():
        wl =  body.getWaveLength()

        body.solveDimensions(guess=1.0)
        body.info()

        #print body.solveSources(f2m(9.0),1.0/7.0)

        downstreamCoordinates = np.linspace(x_offset*2,8*wl,400)

        c.sub(224)
        c.plotWaves(body,downstreamCoordinates, normalize=False)
        body.writeWaves(downstreamCoordinates)

        print 'Wave length = ',wl
    # ------------------------------------------------
    c.present('RankineBodyWaves.png')


