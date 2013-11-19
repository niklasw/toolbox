import os,sys
def readProject(app,projectRoot,cdi,fnc,snc):
    app.newProject(
            CDIFilename= os.path.join(projectRoot,cdi),
            fluidFilename=os.path.join(projectRoot,fnc),
            variablesToLoad=["Density","Static Pressure","Temperature","Total Pressure","X-Velocity","Y-Velocity","Z-Velocity","Velocity Magnitude"]
            )

def calculateCelsius(app):
    project1=app.currentProject
    equation1=project1.newEquation()
    equation1.variables=[]
    equation1.check(text="TemperatureC=temperature-273<<degK>>;")
    equation1.calculateAll()

def setInitView(app):
    project1=app.currentProject
    viewer1=app.currentViewer
    viewer1.backgroundColor="#ffffff"
    project1.boundingBoxShow=False
    viewer1.setZVerticalWindTunnel()
    viewer1.setOrientation("+X")
    viewer1.viewOrientationSaveInPreferences()
    viewer1.setOrientation("+X")
    viewer1.setCameraView(position=(-5.5,-3,1), viewDirection=(1,1,-0.3), upDirection=(0,0,1))
    viewer1.cullingMode="No Culling"

    csysDisplay1=project1.get(name="CsysDisplay1", type="CsysDisplay")
    csysDisplay1.visible=True
    csysDisplay1.positionMode="Free"
    csysDisplay1.size=(0.15, "m")
    csysDisplay1.peakSize=(0.25, "m")
    csysDisplay1.position=( (0.2, 0, 0.7), "m")

    part1=project1.get(name="BODY_complete", type="Part")
    part1.displayMode="Outline"

    return viewer1

def setShowGeomView(app):
    def setDispMode(proj,type='Part',name='BODY_casing',displayMode='Hidden'):
        part=proj.find(type=type,name=name)
        print part
        if part:
            part.displayMode = displayMode

    p=app.currentProject
    v=app.currentViewer
    v.backgroundColor="#ffffff"
    p.boundingBoxShow=False
    v.setCameraView(position=(-5.5,-3,1), viewDirection=(1,1,-0.3), upDirection=(0,0,1))
    v.setCameraView(position=(-5.5,-3,1), viewDirection=(1,1,-0.3), upDirection=(0,0,1))

    # hide all
    i = 0
    while 1:
        try:
            p.getByIndex(i,'Part').displayMode = 'Hidden'
            p.getByIndex(i,'Face').displayMode = 'Hidden'
        except:
            break
        i+=1

    setDispMode(p,type="Part",name="BODY_casing",displayMode="solid")
    setDispMode(p,type="Part",name="BODY_complete",displayMode="Hidden")
    setDispMode(p,type="Part",name="CHAS_plates",displayMode="Solid")
    setDispMode(p,type="Part",name="CHAS_rear_wheels",displayMode="Solid")
    setDispMode(p,type="Part",name="COOL_fan",displayMode="Solid")
    setDispMode(p,type="Part",name="COOL_fan_cover",displayMode="Solid")
    setDispMode(p,type="Face",name="BODY_complete.1",displayMode="Solid")
    setDispMode(p,type="Face",name="BODY_complete.10",displayMode="Solid")
    setDispMode(p,type="Face",name="BODY_complete.19",displayMode="Outline")
    setDispMode(p,type="Face",name="BODY_complete.21",displayMode="Outline")
    setDispMode(p,type="Face",name="BODY_complete.27",displayMode="Outline")

    return v

def saveImage(v,imageName):
    v.saveImage(filename=imageName,size=(1400,1000))

def SaveImage(imageName,overwrite=False,size=(1600,1000)):
    v=app.currentProject.getViewer(0)
    v.saveImage(filename=imageName,size=size,forceOverwrite=overwrite)

def setScalarSets(app):
    fields = {}
    project1=app.currentProject
    fields["Temperature"] = project1.get(name="Temperature", type="ScalarPropertySet")
    fields["Temperature"].range = ( (300, 360), "degK")

    # Validate this before use:
    #eqn = project1.newEquation()
    #eqn.check(text="TemperatureC=temperature-273<<degK>>;")
    #eqn.calculateAll()
    #fields["TemperatureC"] = project1.get(name="TemperatureC", type="ScalarPropertySet")
    #fields["TemperatureC"].range = ( (27, 87), "degK")

    fields["Velocity"] = project1.get(name="Velocity Magnitude", type="ScalarPropertySet")
    fields["Velocity"].range = ( (0,10), "m/sec" )

    fields["Velocity"] = project1.get(name="Velocity Magnitude", type="ScalarPropertySet")
    fields["Velocity"].range = ( (0,10), "m/sec" )

    fields["X-Velocity"] = project1.get(name="X-Velocity", type="ScalarPropertySet")
    fields["X-Velocity"].range = ( (0,10), "m/sec" )

    fields["Y-Velocity"] = project1.get(name="Y-Velocity", type="ScalarPropertySet")
    fields["Y-Velocity"].range = ( (0,10), "m/sec" )

    fields["Z-Velocity"] = project1.get(name="Z-Velocity", type="ScalarPropertySet")
    fields["Z-Velocity"].range = ( (0,10), "m/sec" )

    return fields

def createSlice(app,fields,pos=(0,0,0),size=(1,1,1),align="X",rot=(0,0,0,0),name="X-slice",field="Temperature",writeToFile=False, outDataFile=False):
    p=app.currentProject
    mvs=p.new(type="MovableSlice")
    mvs.orientation = align+"-Aligned"
    mvs.visibility="Hide Bounding Box"
    mvs.name = name
    mvs.imageMode = "Image"
    mvs.position=(pos,"m")
    mvs.size=(size,"m")
    mvs.scalarPropertySet = fields[field]
    mvs.averagesAndIntegralsCalculate=True
    mvs.fluxCalculate=True
    mvs.fluxVolumeFlowRate=True
    if fields and outDataFile:
        averageTemperature = mvs.getAverage(fields["Temperature"])
        averageVelocity = mvs.getAverage(fields["Velocity"])
        print name,"Avg T = ",averageTemperature
        print name,"Avg V = ",averageVelocity
        print name,"Volume flux = ", mvs.fluxIntegral
        if writeToFile:
            outDataFile.write("%s T_avg %s\n" %(name,averageTemperature))
            outDataFile.write("%s V_avg %s\n" %(name,averageVelocity))
            outDataFile.write("%s Volume_flux %s\n" %(name,mvs.fluxIntegral))
    return mvs

def setCoolerView(app):
    v = app.currentViewer
    v.setCameraView(position=(0.4, -3, 0.6), viewDirection=(-0.5,0.8,-0.27), upDirection=(0,0,1))

def generateCoolerSlice(app,fields={}):
    mvs = createSlice(app,fields,
            pos=(-0.857029, -1.117240, -0.119492),
            size=(0.830621, 0.578008, 0.062840),
            align="Y",
            name="Cooler Slice",writeToFile=True)
    setCoolerView(app)
    return mvs

def clearDictObjects(adict):
    for k in adict:
        adict[k].delete()


def hideEngineParts(app):
    p=app.currentProject
    for part,vis in {"CHAS_plates":"Outline","CHAS_silencer":"Hidden","DRV_engine":"Hidden"}.iteritems():
        try:
            p.get(name=part, type="Part").displayMode = vis
        except:
            print "Part",part,"Not found in model"


def setLegends(app,fields):
    legends = {}
    legendVisibility = "Hide Background and Border"

    project1=app.currentProject

    name = "Temperature"
    l=project1.newLegend()
    l.name=name
    l.orientation="Horizontal"
    l.position=(0, -0.5)
    l.significantFigures=0
    l.font=["Nimbus Sans L",12,50,False]
    l.scalarPropertySet=fields["Temperature"]
    l.increment=(5, "degK")
    l.visibility = legendVisibility
    legends[name] = l

    name = "Velocity"
    l=project1.newLegend()
    l.name=name
    l.orientation="Horizontal"
    l.position=(0., -0.5)
    l.significantFigures=0
    l.font=["Nimbus Sans L",12,50,False]
    l.scalarPropertySet=fields["Velocity"]
    l.increment=(5, "m/s")
    l.visibility = legendVisibility
    legends[name] = l

    return legends


def clearDicts(dictList):
    for k in dictList:
        for key in k:
            k[key].delete()

def showHide(alist,hide=False):
    if not hide:
        v="Hide All"
    else:
        v="Hide Bounding Box"
    for key in alist:
        alist[key].visibility = v

def setVisibility(alist,visibility="All Visible"):
    for key in alist:
        alist[key].visibility = visibility

def setScalarProperty(alist, value):
    for key in alist:
        alist[key].scalarPropertySet = value

def generateYSlices(app,imagesDir, fields, field="Temperature"):
    positions = [-0.725,-0.36,0.0,0.36,0.725]
    slices  = {}
    for i,p in enumerate(positions):
        sName = "Ys"+str(i)+"_"+field
        s = createSlice(app,fields,pos=(-1,p,0),align="Y",size=(3.5,2,0.1),field="Temperature",name=sName)
        s.visibility = "Hide BoundingBox"
        slices[sName] = s
        imageName = os.path.join(imagesDir,sName+".png")
        app.currentProject.getViewer(0).saveImage(filename=imageName,size=(1400,1000))
        s.visibility="Hide All"
    return slices

def generateXSlices(app,imagesDir,fields, field="Temperature"):
    positions = [-0.5,-0.8125,-1.125,-1.4375,-1.75]
    slices  = {}
    for i,p in enumerate(positions):
        sName = "Xs"+str(i)+"_"+field
        s = createSlice(app,fields,pos=(p,-0,0),align="X",size=(2.5,2,0.1),field="Temperature",name=sName)
        s.visibility = "Hide BoundingBox"
        slices[sName] = s
        imageName = os.path.join(imagesDir,sName+".png")
        app.currentProject.getViewer(0).saveImage(filename=imageName,size=(1400,1000))
        s.visibility="Hide All"
    return slices


def generateStreamlines(app,fields):
    streamlines = {}
    project1=app.currentProject
    colorMode = "Scalar Property Set"

    # ------------
    sName = 'SL-Rear'
    s = project1.new(type="FluidStreamlines")
    s.visibility        = "Hide All"
    s.rotation          = ( 0,0,1,0 )
    s.position          = ( (0.27, 0.0648457, 0.65), "m")
    s.size              = ( (0.05, 1.5, 0.25), "m")
    s.number            = (3, 40, 10)
    s.scalarPropertySet = fields["Temperature"]
    s.pathStyle         = "Ribbon"
    s.tracingDirection  = "Downstream"
    s.colorMode         = colorMode
    s.numSteps          = 500
    s.name              = sName
    s.ribbonWidth       = ( 0.0075, "m" )

    streamlines[sName] = s
    # ------------

    # ------------
    sName = 'SL-Fan'
    s = project1.new(type="FluidStreamlines")
    s.visibility        = "Hide All"
    s.rotation          = ( 0,0,1,0 )
    s.position          = ( (-0.864743, -0.742785, -0.0557378), "m")
    s.size              = ( (0.07, 0.65, 0.65), "m")
    s.number            = (3, 25,25)
    s.scalarPropertySet = fields["Velocity"]
    s.pathStyle         = "Ribbon"
    s.tracingDirection  = "Downstream"
    s.colorMode         = colorMode
    s.numSteps          = 500
    s.name              = sName
    s.ribbonWidth       = ( 0.0075, "m" )

    streamlines[sName] = s
    # ------------

    # ------------
    sName = 'SL-Cool'
    s = project1.new(type="FluidStreamlines")
    s.visibility        = "Hide All"
    s.rotation          = ( 0,0,1,0 )
    s.position          = ( (-0.85, -1.1475, -0.05), "m")
    s.size              = ( (0.8, 0.02, 0.7), "m")
    s.number            = (20, 1, 20)
    s.scalarPropertySet = fields["Velocity"]
    s.pathStyle         = "Ribbon"
    s.tracingDirection  = "Downstream"
    s.colorMode         = colorMode
    s.numSteps          = 500
    s.name              = sName
    s.ribbonWidth       = ( 0.0075, "m" )

    streamlines[sName] = s
    # ------------

    # ------------
    sName = 'SL-Exhaust'
    s = project1.new(type="FluidStreamlines")
    s.visibility        = "Hide All"
    s.setPositionRotation(trans=(-0.2199999988, -0.3531444371, -0.4499999881), rot=(1.591421e-15,-1.000000e+00,-1.629207e-07,1.399862e-01))
    s.position          = ( (-0.22, -0.34, -0.45), "m")
    s.size              = ( (0.17, 0.125, 0.02), "m")
    s.number            = (15, 15, 2)
    s.scalarPropertySet = fields["Temperature"]
    s.pathStyle         = "Ribbon"
    s.tracingDirection  = "Downstream"
    s.colorMode         = colorMode
    s.numSteps          = 500
    s.name              = sName
    s.ribbonWidth       = ( 0.0075, "m" )

    streamlines[sName] = s
    # ------------

    return streamlines


def saveStrlImages(app,imagesDir, baseName):
    project1=app.currentProject
    viewer1=project1.getViewer(0)
    fname=os.path.join(imagesDir,baseName)
    viewer1.setCameraView(position=(-2, 0.6, 3.6), viewDirection=(0.25, -0.2, -0.95), upDirection=(0.1, -0.97, 0.23))
    viewer1.saveImage(filename=fname+"_1.png",size=(1400,1000))

    viewer1.setOrientation("-X")
    viewer1.cameraPosition=( (4,0,0), "m")
    viewer1.saveImage(filename=fname+"_2.png",size=(1400,1000))

    viewer1.setOrientation("+Y")
    viewer1.cameraPosition=( (-0.8, -4, 0), "m")
    viewer1.saveImage(filename=fname+"_3.png",size=(1400,1000))

    viewer1.setOrientation("-Y")
    viewer1.cameraPosition=( (-0.8, 4, 0), "m")
    viewer1.saveImage(filename=fname+"_4.png",size=(1400,1000))

    viewer1.setOrientation("-Z")
    viewer1.cameraPosition=( (-0.8, -0.4, 4.0), "m")
    viewer1.saveImage(filename=fname+"_5.png",size=(1400,1000))

    viewer1.setOrientation("+Z")
    viewer1.cameraPosition=( (-0.8, -0.4, -4.0), "m")
    viewer1.saveImage(filename=fname+"_6.png",size=(1400,1000))

    viewer1.setCameraView(position=(-1.8, -2.4, 1.2), viewDirection=(0.25, 0.8, -0.5), upDirection=(0,0,1))
    viewer1.setCameraView(position=(-1.8, -2.4, 1.2), viewDirection=(0.25, 0.8, -0.5), upDirection=(0,0,1))
    viewer1.saveImage(filename=fname+"_7.png",size=(1400,1000))

    viewer1.setCameraView(position=(-0.2, -2.5, -1.3), viewDirection=(-0.3, 0.8, 0.4), upDirection=(0,0, 1))
    viewer1.setCameraView(position=(-0.2, -2.5, -1.3), viewDirection=(-0.3, 0.8, 0.4), upDirection=(0,0, 1))
    viewer1.saveImage(filename=fname+"_8.png",size=(1400,1000))

    viewer1.setCameraView(position=(-1.8, 2.8, -2), viewDirection=(0.25, -0.8, 0.5), upDirection=(0,0,1))
    viewer1.setCameraView(position=(-1.8, 2.8, -2), viewDirection=(0.25, -0.8, 0.5), upDirection=(0,0,1))
    viewer1.saveImage(filename=fname+"_9.png",size=(1400,1000))

    viewer1.setCameraView(position=(-3.0, 2.0, 1.5), viewDirection=(0.5, -0.7, -0.6), upDirection=(0,0,1))
    viewer1.setCameraView(position=(-3.0, 2.0, 1.5), viewDirection=(0.5, -0.7, -0.6), upDirection=(0,0,1))
    viewer1.saveImage(filename=fname+"_10.png",size=(1400,1000))


# ------------------------------------------------------------------------




