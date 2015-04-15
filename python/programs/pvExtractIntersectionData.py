#!/usr/bin/env pvbatch

import sys
from os.path import splitext

#### import the simple module from the paraview
from paraview.simple import *
#paraview.simple._DisableFirstRenderCameraReset()


# Check number of arguments. If two, expect the second to
# be an STL file

haveStl = False
if len(sys.argv) == 2:
    haveStl = True

vtkWaveFile = sys.argv[1]
vtkWaveFileBase = splitext(vtkWaveFile)[0]
csvWaveFile = vtkWaveFileBase+'.csv'

# create a new 'Legacy VTK Reader'
alphavtk = LegacyVTKReader(FileNames=[vtkWaveFile])

# create a new 'Elevation'
elevation1 = Elevation(Input=alphavtk)

# Properties modified on elevation1
elevation1.LowPoint = [100.0, 0.0, 11.328574180603027]
elevation1.HighPoint = [100.0, 0.0, 12.59897232055664]

# get color transfer function/color map for 'Elevation'
# elevationLUT = GetColorTransferFunction('Elevation')

# create a new 'Plot On Intersection Curves'
plotOnIntersectionCurves1 = PlotOnIntersectionCurves(Input=elevation1)
plotOnIntersectionCurves1.SliceType = 'Plane'

# init the 'Plane' selected for 'SliceType'
plotOnIntersectionCurves1.SliceType.Origin = [100.0, 0.0, 11.963773250579834]

# Properties modified on plotOnIntersectionCurves1.SliceType
plotOnIntersectionCurves1.SliceType.Normal = [0.0, 1.0, 0.0]

# save data
SaveData(csvWaveFile, proxy=plotOnIntersectionCurves1, UseScientificNotation=1)


# OK, data extracted to disk.
# Problem is; Paraview for some reason generates an unknown number of data sets,
# some of which overlaps, during the plotOnIntersectionLine.
# Each data set is written to a separate, numbered file. Now, these files need
# to be concatenated, sorted and plotted.

from numpy import array, loadtxt, concatenate, savetxt, transpose
from matplotlib import pyplot as plt
from glob import glob

csvGlob = vtkWaveFileBase+'*.csv'
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

a = sorted(allData, key=lambda a_entry: a_entry[2])
allData = array(a)

xzData = allData[:,(2,4)]

savetxt(vtkWaveFileBase+'.dat',xzData)

plt.plot(xzData[:,0], xzData[:,1])
plt.grid()
plt.savefig('test.png')

