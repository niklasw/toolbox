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
    u_inf = 2 #f2m(10)                 # 10 feet/s    Shaffer page 13
    x_offset = f2m(4.18)            # 4.18 ft from Shaffer page 5
    y_offset = 0.0
    clDepth      = 0.72 #f2m(3)           # 3 feet    Shaffer page 13
    sourceFactor = 0.104            # From page 5 in Shaffer ( 4*pi ??)

    L = 3.0 #f2m(9)
    aspect = 1.0/8

    Mesh = mesh(-L,L,-L/2,L/2,600,300)

    fs = freeStream(u_inf,0.0,Mesh)

    pos0 = (.0,.0)
    body = rankine(L,aspect,pos0,fs,clDepth)

    body.info()

    size = 15
    figureSize = (size, (Mesh.dimensions()[1])/(Mesh.dimensions()[0])*size)

    c = canvas(body.sources)

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

        body.info()

        #print body.solveSources(f2m(9.0),1.0/7.0)

        downstreamCoordinates = np.linspace(x_offset*2,8*wl,400)

        c.sub(224)
        c.plotWaves(body,downstreamCoordinates, normalize=False)
        body.writeWaves(downstreamCoordinates)


        print 'Wave length = ',wl
    # ------------------------------------------------
    c.present('RankineBodyWaves.png')

