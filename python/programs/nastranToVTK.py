#!/usr/bin/python

import sys,vtk

def readGeometry(fileName,geometryDict):
    geometryDict['GRID'] = []
    geometryDict['TRIA'] = []
    geometryDict['QUAD'] = []
    
    try:
        with open(fileName) as fp:
            datData= fp.readlines()
    except:
        print 'Failed to open geometry input'

    def readVertex(line,tag,geom):
        if line[0:len(tag)] == tag: 
            gridNo = int(line[8:17].strip())
            verts = map(float,(line[18:32], line[32:40], line[40:49]))
            geom[tag].append(verts)

    def readFace(line,tag,geom):
        if line[1:5] == tag:
            elemNo = int(line[9:16])
            if tag == 'TRIA':
                points = map(int,(line[25:32],line[32:40],line[40:48]))
            else:
                points = map(int,(line[25:32],line[32:40],line[40:48],line[48:56]))
            # Decrease id -1 due to fortran notation
            points = [ p-1 for p in points]
            geom[tag].append(points)

    for line in datData:
            readVertex(line,'GRID',geometryDict)
            readFace(line,'TRIA',geometryDict)
            readFace(line,'QUAD',geometryDict)
    
    print 'Finished geometry.'
    print 'Extracted from file:'
    print '\tpoints {0}'.format(len(geometryDict['GRID']))
    print '\ttrias  {0}'.format(len(geometryDict['TRIA']))
    print '\tquads  {0}'.format(len(geometryDict['QUAD']))


def readModes(fileName, shapesDict):
    print '\nReading modes.'
    modeNo = -1
    with open(fileName) as fp:
        while 1:
            try:
                line=fp.next()
                if line[1:11] == 'EIGENVALUE':
                    modeNo = int(line.split()[5])
                    shapesDict[modeNo] = []
                    line = fp.next()
                if modeNo != -1:
                    try:
                        v0 = map(float, line.split()[2:5])
                        line = fp.next()
                        v1 = map(float, line.split()[1:4])
                        #shapesDict[modeNo].append((v0,v1))
                        shapesDict[modeNo].append(v0)
                    except:
                        continue
            except:
                print 'EOF', modeFileName
                break
    
    print 'Finished modes.'
    print 'Extracted from file:'
    print '\t{0} modes'.format(modeNo)

def convertGeometry(geometry):
    nGeometryPoints = len(geometry['GRID'])
    _vtkPoints = vtk.vtkPoints()
    _vtkPoints.SetNumberOfPoints(nGeometryPoints)
    
    for i,p in enumerate(geometry['GRID']):
        _vtkPoints.InsertPoint(i,p)
    
    def addMeshElements(nasFaces, vtkFaces, f=vtk.vtkTriangle):
        for face in nasFaces:
            vtkFace = f()
            for i,id in enumerate(face):
                vtkFace.GetPointIds().SetId(i,id)
            vtkFaces.InsertNextCell(vtkFace)
    
    _vtkFaces = vtk.vtkCellArray()
    
    addMeshElements(geometry['TRIA'], _vtkFaces, vtk.vtkTriangle)
    addMeshElements(geometry['QUAD'], _vtkFaces, vtk.vtkQuad)
    
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(_vtkPoints)
    polyData.SetPolys(_vtkFaces)

    return polyData

def addModeData(shapes,polyData):
    for modeName in shapes.keys():
        print modeName, len(shapes[modeName])
        _vtkDisplacement = vtk.vtkFloatArray()
        _vtkDisplacement.SetNumberOfComponents(3)
        _vtkDisplacement.SetName('Mode_{0:03d}'.format(modeName))
        #_vtkDisplacement.SetName('Mode_%03d'%modeName)
        for displacement in shapes[modeName]:
            dx,dy,dz = displacement
            _vtkDisplacement.InsertNextTuple3(dx,dy,dz)
    
        polyData.GetPointData().AddArray(_vtkDisplacement)



datFileName = sys.argv[1]
modeFileName = sys.argv[2]

geometry = dict()
shapes = dict()

readGeometry(datFileName,geometry)
readModes(modeFileName, shapes)

_vtkPolyData = convertGeometry(geometry)
addModeData(shapes,_vtkPolyData)
   

_vtkPolyData.Modified()

writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName('data.vtp')
writer.SetInputData(_vtkPolyData)
writer.Write()


