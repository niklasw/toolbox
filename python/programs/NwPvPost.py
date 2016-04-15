#!/usr/bin/env pvbatch

import os,sys

try:
    try: paraview.simple
    except: from paraview.simple import *
    paraview.simple._DisableFirstRenderCameraReset()
except:
    print 'Paraview API not found'
    sys.exit(1)



class Setup:
    SCALAR_FIELD    = 'k'
    FIELD_FUNCTION  = 'mag(U)'
    SCALAR_MIN      = 0
    SCALAR_MAX      = 2
    NORMAL          = (0,1,0)
    ORIGIN          = (0.0,0.0,0.0)
    CAMERA_UP       = (0,0,1)
    CAMERA_POS      = (2.0,-50,0)
    CAMERA_FOCUS    =  (2.0,0.0,0.0)
    CAMERA_ZOOM     = 1
    IMAGE_SCALE     = 1
    VIEW_SIZE       = [8000,1000]
    LEGEND          = True
    FIELDMODE        = 'POINTS'

    def __init__(self):
        pass

from NwPvTools import NwPvTools, Field

if __name__=="__main__":

    setup = Setup()

    pvt = NwPvTools('setup.foam')
    pvt.initFromSetup(setup)
    pvt.source.CaseType = 'Decomposed Case'

    Hide()
    pvt.createSlice(origin=setup.ORIGIN,normal=setup.NORMAL)
    pvt.calculator()
    pvt.legend(setup.LEGEND)
    Show()
    pvt.saveFig('testFig_magU',setup.IMAGE_SCALE)

    setup.FIELD_FUNCTION='sqrt(k)'
    setup.SCALAR_MAX=0.1

    pvt.field.initFromSetup(setup)
    pvt.calculator()
    pvt.legend(setup.LEGEND)
    Show()

    pvt.saveFig('testFig_k',setup.IMAGE_SCALE)
    #pvt.animate('testAnim',setup.IMAGE_SCALE)

