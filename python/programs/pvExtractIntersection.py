#!/usr/bin/env pvbatch

import sys, os
from os.path import splitext,isfile

#### import the simple module from the paraview
from paraview.simple import *
#paraview.simple._DisableFirstRenderCameraReset()

def Error(self,s,sig=1):
    print '\nError %s!\n' % s
    sys.exit(sig)

def Warn(self,s):
    output = 'Warning %s!' % s
    print '\n'+'='*len(output)
    print output
    print '='*len(output)

def Info(self,s):
    print '\t%s' % s

class stringVector(list):
    def __init__(self,sv):
        self.istring = sv.strip()
        #self.vector = self.convert()
        list.__init__(self,self.convert())

    def convert(self, test=float):
        nstring = self.istring.strip('()').split()
        floatList = map(test, nstring)
        return floatList


def getArgs():
    from optparse import OptionParser
    from optparse import Values as optValues
    descString = """
    ParaView python script that extracts x z data from the intersection
    between a plane (origin, normal) and a VTK surface
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--vtk',dest='vtk',default=None,help='Input vtk file')
    parser.add_option('-t','--stl',dest='stl',default=None,help='Optional stl file')
    parser.add_option('-n','--normal',dest='normal',default='(0 1 0)',help='Intersection plane normal "(0 1 0)"')
    parser.add_option('-o','--origin',dest='origin',default='(0 0 0)',help='Intersection plane origin "(0 0 0)"')

    options,arguments = parser.parse_args()

    if not getattr(options,'vtk'):
        print 'Missing -f'
    else:
        if os.path.isfile(options.vtk):
            options.vtk = os.path.join(os.getcwd(),options.vtk)
        else:
            argError('No such file %s'% options.vtk)

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)

    def validateOption(opts,optName, test, msg='Invalid argument', allowed=[]):
        option = getattr(opts,optName)
        try: setattr(opts,optName,test(option))
        except: argError('%s; got %s' % (msg,option))
        if allowed and not option in allowed:
            argError('%s; got %s. Allowed values are %s' % (msg,option,allowed))
        return option

    validateOption(options,'normal', stringVector)
    validateOption(options,'origin', stringVector)
    return options,arguments



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


opt,arg = getArgs()

print opt.normal
print opt.origin

vtkWaveFile = opt.vtk
vtkWaveFileBase = splitext(vtkWaveFile)[0]
csvWaveFile = vtkWaveFileBase+'.csv'

# create a new 'Legacy VTK Reader'
alphavtk = LegacyVTKReader(FileNames=[vtkWaveFile])

extractIntersectionData(alphavtk, fileNameBase=vtkWaveFileBase, normal=opt.normal,origin=opt.origin)

xzData = reduceData(vtkWaveFileBase)

if opt.stl:
    print 'Reading STL data'
    stlFile = opt.stl
    stlFileBase = splitext(stlFile)[0]
    csvStlFile = stlFileBase+'.csv'
    stlvtk = STLReader(FileNames=[stlFile])
    extractIntersectionData(stlvtk, fileNameBase=stlFileBase, normal=opt.normal, origin=opt.normal)
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

