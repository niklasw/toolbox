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
                points = [int(a) for a in (line[25:32],line[32:40],line[40:48])]
            elif tag == 'QUAD':
                points = [int(a) for a in (line[25:32],line[32:40],line[40:48],line[48:56])]
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
                print 'Read {0} arrays from data file'.format(modeNo)
                break


def convertGeometry(geometry):
    '''Creates, fill and return a vtkPolyData object'''
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

    print 'Geometry converted to vtkPolyData object'

    return polyData

def addModeData(shapes,polyData):
    '''Append mode data (vector array) to vtkPolyData object'''
    for modeName in shapes.keys():
        _vtkDisplacement = vtk.vtkFloatArray()
        _vtkDisplacement.SetNumberOfComponents(3)
        _vtkDisplacement.SetName('Mode_{0:03d}'.format(modeName))
        for displacement in shapes[modeName]:
            dx,dy,dz = displacement
            _vtkDisplacement.InsertNextTuple3(dx,dy,dz)

        polyData.GetPointData().AddArray(_vtkDisplacement)
    print 'Added {0} arrays to vtk object'.format(len(shapes.keys()))


def addCylTransformedData(shapes,polyData):
    '''Append mode data (vector array) to vtkPolyData object'''
    from numpy import array,sin,cos,sqrt,arctan2
    for modeName in shapes.keys():
        _vtkDisplacement = vtk.vtkFloatArray()
        _vtkDisplacement.SetNumberOfComponents(3)
        _vtkDisplacement.SetName('cylMode_{0:03d}'.format(modeName))
        axis = array([1,0,0])

        for displacement in shapes[modeName]:
            dx,dy,dz = displacement
            dr = sqrt(dy**2+dz**2)
            dphi = arctan2(dz,dy)
            _vtkDisplacement.InsertNextTuple3(dr,dphi,dx)

        polyData.GetPointData().AddArray(_vtkDisplacement)
    print 'Added {0} arrays to vtk object'.format(len(shapes.keys()))



from os.path import splitext

datFileName = sys.argv[1]
modeFileName = sys.argv[2]
vtkFileName = splitext(datFileName)[0]+'.vtp'

geometry = dict()
shapes = dict()

readGeometry(datFileName,geometry)
readModes(modeFileName, shapes)

_vtkPolyData = convertGeometry(geometry)
addModeData(shapes,_vtkPolyData)
#addCylTransformedData(shapes,_vtkPolyData)


_vtkPolyData.Modified()

print 'Writing vtk file {0}'.format(vtkFileName)
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(vtkFileName)
writer.SetInputData(_vtkPolyData)
writer.Write()
print 'End.'


