#!/usr/bin/python

import sys
from potentialFlow import mesh,source,freeStream,sourceList,rankine,canvas
from matplotlib import pyplot as plt
import numpy as np

def f2m(l):
    return l*0.3048
def m2f(m):
    return m/0.3048
def m2inch(l):
    return m2f(l)*12


def runOneCondition(u_inf=f2m(10), clDepth = f2m(3), L = f2m(9), aspect = 1.0/7,doPlots=False):
    ## Settings for Shaffers 9 ft 7/1 body
    # 10 feet/s           Shaffer page 13
    # 3 feet submersion   Shaffer page 13

    Mesh = mesh(-L,L,-L/2,L/2,1200,800)

    fs = freeStream(u_inf,0.0,Mesh)

    pos0 = (.0,.0)
    body = rankine(L,aspect,pos0,fs,clDepth)

    body.info()
    waveLength =  body.getWaveLength()

    # -Rankine Body ----------------------------------
    sourceOffset = abs(body.sources[0].x)
    downstreamCoordinates = np.linspace(sourceOffset,8*waveLength,400)
    waveMax = max(body.waves(downstreamCoordinates))
    waveMin = min(body.waves(downstreamCoordinates))
    print 'Max wave elevation = {0:8.2e} m'.format(waveMax)
    print 'Min wave elevation = {0:8.2e} m'.format(waveMin)
    #body.writeWaves(downstreamCoordinates)

    if doPlots:
        size = 15
        figureSize = (size, (Mesh.dimensions()[1])/(Mesh.dimensions()[0])*size)
        c = canvas(body.sources)
        c.new(figureSize)
        c.plotPotentialFlow()
        c.sub(224)
        c.plotWaves(body,downstreamCoordinates, normalize=False)
        c.present('RankineBodyWaves.png')

    return waveMax, waveLength


if __name__=='__main__':

    velocities = [f2m(a) for a in np.arange(2,12,(12-2.0)/100)]
    depths     = [f2m(a) for a in [1,1.5,2]]
    bodyLength = f2m(4.5)
    aspectRatio = 1.0/7.0
    for d in depths:
        with open('rankineWaveData_{0:0.01f}ft.dat'.format(d),'w') as fp:
            fp.write('#{0} {1} {2} {3}\n'.format("depth","velocity","waveMax","waveLength"))
            for v in velocities:
                wh,wl = runOneCondition(
                       L=bodyLength,
                       aspect=aspectRatio,
                       u_inf=v,
                       clDepth=d,
                       doPlots=False)
                fp.write('{0} {1} {2} {3}\n'.format(d,v,wh,wl))
                #fp.write('{0} {1} {2} {3}\n'.format(m2f(d),m2f(v),m2inch(wh),m2f(wl)))


