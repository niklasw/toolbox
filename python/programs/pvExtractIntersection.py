#!/usr/bin/env pvbatch

import sys, os
from os.path import splitext

#### import the simple module from the paraview
from paraview.simple import *
#paraview.simple._DisableFirstRenderCameraReset()

def extractIntersectionData(node,origin=[0,0,0],normal=[0,1,0],fileNameBase='data'):
    '''Using paraview python bindings to extract data
    from a surface along an intersection with a plane'''

    # create a new 'Plot On Intersection Curves'
    plotOnIntersectionCurves1 = PlotOnIntersectionCurves(Input=node)
    plotOnIntersectionCurves1.SliceType = 'Plane'

    # init the 'Plane' selected for 'SliceType'
    plotOnIntersectionCurves1.SliceType.Origin = origin

    # Properties modified on plotOnIntersectionCurves1.SliceType
    plotOnIntersectionCurves1.SliceType.Normal = normal

    # save data
    SaveData(fileNameBase+'.csv', proxy=plotOnIntersectionCurves1, UseScientificNotation=1)

def reduceData(fileNameBase='data', sortData=True):
    # OK, data extracted to disk.
    # Problem is; Paraview for some reason generates an unknown number of data sets,
    # some of which overlaps, during the plotOnIntersectionLine.
    # Each data set is written to a separate, numbered file. Now, these files need
    # to be concatenated, sorted and plotted.

    try:
        from numpy import array, loadtxt, concatenate, savetxt, transpose
    except:
        print 'Error: cannot find required python module \'numpy\'.'
        sys.exit(1)

    from glob import glob

    csvGlob = fileNameBase+'*.csv'
    csvFiles = glob(csvGlob)

    # Read file header, just to print it, for debugging...
    with open(csvFiles[0]) as fp:
        print fp.readline()

    allData = None
    for f in csvFiles:
        dataSet = loadtxt(f,skiprows=1,delimiter=',')
        if allData == None:
            allData = dataSet.copy()
        else:
            allData = concatenate((allData, dataSet))
            print 'Adding data set size', dataSet.shape
            print ''
        os.remove(f)

    if sortData:
        a = sorted(allData, key=lambda a_entry: a_entry[1])
        allData = array(a)
    xzData = allData[:,(1,3)]
    savetxt(fileNameBase+'.dat',xzData)
    return xzData

# Check number of arguments. If two, expect the second to
# be an STL file

haveStl = False
if len(sys.argv) == 3:
    haveStl = True

vtkWaveFile = sys.argv[1]
vtkWaveFileBase = splitext(vtkWaveFile)[0]
csvWaveFile = vtkWaveFileBase+'.csv'

# create a new 'Legacy VTK Reader'
alphavtk = LegacyVTKReader(FileNames=[vtkWaveFile])

extractIntersectionData(alphavtk, fileNameBase=vtkWaveFileBase, normal=[0,1,0],origin=[0,0,0])

xzData = reduceData(vtkWaveFileBase)

if haveStl:
    print 'Reading STL data'
    stlFile = sys.argv[2]
    stlFileBase = splitext(stlFile)[0]
    csvStlFile = stlFileBase+'.csv'
    stlvtk = STLReader(FileNames=[stlFile])
    extractIntersectionData(stlvtk, fileNameBase=stlFileBase, normal=[0,1,0], origin=[0,0,0])
    xzStlData = reduceData(stlFileBase, sortData=False)

havePlt = False
try:
    from matplotlib import pyplot as plt
    havePlt = True
except:
    print 'Warning: plotting is not available, sonce matplotlib failed to import'

if havePlt:
    plt.plot(xzData[:,0], xzData[:,1])
    plt.grid()
    plt.savefig('test.png')

