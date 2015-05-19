#!/usr/bin/env pvbatch

import sys, os
from os.path import splitext,isfile
from os.path import join as pjoin

#### import the simple module from the paraview
from paraview.simple import *
#paraview.simple._DisableFirstRenderCameraReset()

def Error(s,sig=1):
    print '\nError %s!\n' % s
    sys.exit(sig)

def Warn(s):
    output = 'Warning %s!' % s
    print '\n'+'='*len(output)
    print output
    print '='*len(output)

def Info(s):
    print '\t%s' % s

def isFile(f):
    path = pjoin(os.getcwd(),f)
    if not os.path.isfile(path):
        Error('Cannot find file {0}'.format(f))
    else:
        return path

def checkSuffix(f,suffix='vtk'):
    path = isFile(f)
    if not os.path.splitext(path)[1] == suffix:
        Error('Input file {0} has wrong suffix. Should be {1}'.format(f,suffix))
    else:
        return path

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
    between a plane (origin, normal) and a VTK surface. Optionally
    an STL surface can be defined as well (e.g. the hull geometry from
    which a profile will be generated.)
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--vtk',dest='vtk',default=None,help='Input vtk file')
    parser.add_option('-t','--stl',dest='stl',default=None,help='Optional stl file')
    parser.add_option('-n','--normal',dest='normal',default='(0 1 0)',help='Intersection plane normal "(0 1 0)"')
    parser.add_option('-o','--origin',dest='origin',default='(0 0 0)',help='Intersection plane origin "(0 0 0)"')

    options,arguments = parser.parse_args()

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)

    def checkFileOption(o,suffix):
        option = getattr(options,o)
        if not option:
            argError('Missing option {0}'.format(o))
        else:
            setattr(options,o,checkSuffix(option,suffix))

    def validateOption(opts,optName, test, msg='Invalid argument', allowed=[]):
        option = getattr(opts,optName)
        try: setattr(opts,optName,test(option))
        except: argError('%s; got %s' % (msg,option))
        if allowed and not option in allowed:
            argError('%s; got %s. Allowed values are %s' % (msg,option,allowed))
        return option

    checkFileOption('vtk','.vtk')
    checkFileOption('stl','.stl')

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

    def getColNo(header,c1,c2):
        '''Assume csv header and search for index of searchStr'''
        hList = [a.strip('" \n') for a in header.split(',')]
        try:
            col1 = hList.index(c1)
            col2 = hList.index(c2)
        except:
            Warn('Could not find column index in file. Guessing 1 and 3')
            col1 = 1
            col2 = 3
        return (col1, col2)

    try:
        from numpy import array, loadtxt, concatenate, savetxt, transpose
    except:
        Error('cannot find required python module \'numpy\'.')

    from glob import glob

    csvGlob = fileNameBase+'*.csv'
    csvFiles = glob(csvGlob)

    # Read file header, just to print it, for debugging...
    fileHeader = ''
    with open(csvFiles[0]) as fp:
        Info('Columns defined in file header')
        fileHeader = fp.readline()
        Info(fileHeader)

    useColumns = getColNo(fileHeader,'Points:0','Points:2')
    Info('Using columns {0[0]} and {0[1]} (first column is 0).\n'.format(useColumns))

    allData = None
    for f in csvFiles:
        dataSet = loadtxt(f,skiprows=1,delimiter=',')
        if allData == None:
            allData = dataSet.copy()
            Info('Adding data set size {0}'.format(dataSet.shape))
        else:
            allData = concatenate((allData, dataSet))
            Info('Adding data set size {0}'.format(dataSet.shape))
        os.remove(f)

    if sortData:
        a = sorted(allData, key=lambda a_entry: a_entry[1])
        allData = array(a)
    xzData = allData[:,useColumns]
    Info('Writing xz profile data to '+fileNameBase+'.dat')
    savetxt(fileNameBase+'.dat',xzData)
    return xzData


opt,arg = getArgs()

Info('\nReading VTK data')
vtkWaveFile = opt.vtk
vtkWaveFileBase = splitext(vtkWaveFile)[0]
csvWaveFile = vtkWaveFileBase+'.csv'
pngWaveFile = vtkWaveFileBase+'_profile.png'

alphavtk = LegacyVTKReader(FileNames=[vtkWaveFile])
extractIntersectionData(alphavtk, fileNameBase=vtkWaveFileBase, normal=opt.normal,origin=opt.origin)
xzData = reduceData(vtkWaveFileBase)

Info('\nReading STL data')
stlFile = opt.stl
stlFileBase = splitext(stlFile)[0]
csvStlFile = stlFileBase+'.csv'

stlvtk = STLReader(FileNames=[stlFile])
extractIntersectionData(stlvtk, fileNameBase=stlFileBase, normal=opt.normal, origin=opt.origin)
xzStlData = reduceData(stlFileBase, sortData=False)

havePlt = False
try:
    from matplotlib import pyplot as plt
    havePlt = True
except:
    Warn('Plotting is not available, sonce matplotlib failed to import')

if havePlt:
    plt.plot(xzData[:,0], xzData[:,1])
    plt.plot(xzStlData[:,0], xzStlData[:,1])
    plt.grid()
    Info('Saving TEST plot to image file {0}'.format(pngWaveFile))
    plt.savefig(pngWaveFile)
