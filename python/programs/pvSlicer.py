#!/usr/bin/env pvbatch

import os,sys

import importlib
try:
    try: paraview.simple
    except: from paraview.simple import *
    paraview.simple._DisableFirstRenderCameraReset()
except:
    print 'Paraview API not found'
    sys.exit(1)

def getArgs():
    # This function has nothing to do with Paraview really.
    # Just collecting user input to the script.
    from optparse import OptionParser
    descString = """
    Python thing relying on the paraview API to generate image from data file
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--data',dest='data',default=None,help='Input data file')
    parser.add_option('-o','--image',dest='image',default=None,help='Output image file. No extension! e.g. -o image')
    parser.add_option('-s','--state',dest='state',default=None,help='Input state file')
    parser.add_option('-c','--source',dest='source',default=None,help='Source to slice, if state loaded.')
    parser.add_option('-t','--setup',dest='setup',default='sliceInput.py',help='Plane setup file')

    (opt,arg)=parser.parse_args()

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)

    if opt.data and opt.state:
        argError('Sorry, you must select either state OR file input')

    if opt.state and not opt.source:
        argError('You must name which source to operate on if you load a state')

    if not opt.data and not opt.state:
        argError('Missing data file argument')

    input = [ i for i in (opt.data,opt.state) if i ][0]

    if not os.path.isfile(input):
        argError('Cannot find input %s' % input)

    # Read scene and plane settings from python input file (-d)
    settingsFile = os.path.join(os.getcwd(),opt.setup)
    if not os.path.isfile(settingsFile):
        argError('Cannot find plane setup file\n>> %s' % opt.setup)
    print 'Setup file is:\n>> %s' % settingsFile
    settingsFile = os.path.splitext(settingsFile)[0]
    settingsDir, settingsFile = os.path.split(settingsFile)
    opt.Setup = importlib.import_module(settingsFile)

    if not opt.image:
        argError('Missing image file argument')

    return opt


def loadState(stateFile, activeSource=''):
    servermanager.LoadState(stateFile)
    source = FindSource(activeSource)
    if not source:
        print 'Cannot find data source %s in the state:' % activeSource
        print 'Available sources are:\n'
        for s in GetSources():
            print s[0]
        sys.exit(1)
    SetActiveSource(source)
    return source

def loadCase(dataFile):
    """docstring for loadCasefname"""

    OpenDataFile(dataFile)
    sourcesDict = GetSources()
    source = sourcesDict.values()[0]
    # Set the first source (can it be more than one at
    # this stage??) to active source
    SetActiveSource(source)
    return source

def latestTime(source):
    return source.TimestepValues[-1]

def hideDefaultRepresentation():
    DataRepresentation1 = GetDisplayProperties(source)
    DataRepresentation1.Visibility = 0


def createSlice(origin = (0,0,0), normal = (0,1,0), setActive=True):
    mySlice = Slice(SliceType='Plane')
    mySlice.SliceType.Origin = origin
    mySlice.SliceType.Normal = normal
    if setActive: # (Do not know if this nedded)
        SetActiveSource(mySlice)
    return mySlice

def createVectorRange(startV=(0,0,0), endV=(1,1,1), N=5):
    # Just a pythonic way to create a list of vectors between
    # sweepStart and sweepEnd. I know it looks funny.
    startV = map(float,startV)
    endV = map(float,endV)
    return  ( [a+n*(b-a)/N for a,b in zip(startV,endV)] for n in range(N+1) )

def createScalarRepresentation(scalarName='p',min=-1000,max=1000):
    rep = Show()
    rep.SelectionPointFieldDataArrayName = scalarName
    rep.SelectionCellFieldDataArrayName = scalarName
    rep.ColorArrayName = scalarName
    colorBar = [min, 0.0, 0.0, 1.0, max, 1.0, 0.0, 0.0]
    lookupTable = GetLookupTableForArray( scalarName, 1, RGBPoints=colorBar)
    rep.LookupTable = lookupTable
    return rep

def setView(view, up=(0,1,0),pos=(1,1,1),focus=(0,0,0),scale=1,parallel=1,clip=(-10,10)):
    view.CameraViewUp = up
    view.CameraPosition = pos
    view.CameraClippingRange = clip
    view.CameraFocalPoint = focus
    view.CameraParallelProjection = parallel
    view.CameraParallelScale = scale

def initDisplayAndTime(source,view, bg=[1,1,1,]):
    SetActiveView(view)
    GetDisplayProperties(view=view)
    try:
        #Set to latest time if possible
        view.ViewTime = latestTime(source)
        print 'Time set to latest time: %f' % latestTime(source)
    except:
        #Do nothing
        pass

    view.UseOffscreenRendering=1
    view.UseOffscreenRenderingForScreenshots=1
    view.Background = bg

    return view

def main():

    options = getArgs()
    setup = options.Setup
    image = options.image

    source = None
    if options.data:
        source = loadCase(options.data)
    else:
        source = loadState(options.state,options.source)

    print 'Active source = %s' % source

    sliceOrigins = createVectorRange(startV=setup.SLICES_START, endV=setup.SLICES_END, N=setup.N_SLICES)

    thisView = GetRenderView()

    thisView = initDisplayAndTime(source,thisView)

    scale = 1.0/setup.CAMERA_ZOOM

    if not options.state:
        setView(thisView,scale=scale,pos=setup.CAMERA_POS,focus=setup.CAMERA_FOCUS,up=setup.CAMERA_UP)

    mySlice = createSlice(origin=(0,0,0), normal=setup.NORMAL)

    createScalarRepresentation(scalarName=setup.SCALAR_FIELD,min=setup.SCALAR_MIN,max=setup.SCALAR_MAX)

    for i,origin in enumerate(sliceOrigins):
        viewImage = '%s_view%02d%s' % (image,i,'.png')
        print "%4i %25s slice origin = %s" %(i, viewImage, str(origin))
        mySlice.SliceType.Origin = origin
        Render()
        thisView.WriteImage(viewImage,'vtkPNGWriter',1)

if __name__=='__main__':
    main()

