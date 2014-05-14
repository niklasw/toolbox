#!/usr/bin/python

import sys

datFileName = sys.argv[1]
modeFileNAme = sys.argv[2]


datPtr = open(datFileName)
modesPtr = open(modeFileNAme)

#- never mind RAM. Read it all
datData= datPtr.readlines()

datPtr.close()

geometry = {}

geometry['GRID'] = []
geometry['TRIA'] = []
geometry['QUAD'] = []

# mode data dict:
#   eigenvals = list(float,...)
eigenvals = list()
shapes = dict() #dict(modeNo:(displacement,cont)))

for line in datData:
    if line[0:4] == 'GRID':
        gridNo = int(line[8:17].strip())
        vert = map(float,(line[18:32], line[32:40], line[40:49]))
        geometry['GRID'].append(vert)

    if line[0:6] == 'CTRIA3':
        elemNo = int(line[9:16])
        points = map(int,(line[25:32],line[32:40],line[40:48]))
        # Decrease id -1 due to fortran notation
        points = [ p-1 for p in points]
        geometry['TRIA'].append(points)

    if line[0:6] == 'CQUAD4':
        elemNo = int(line[9:16])
        points = map(int,(line[25:32],line[32:40],line[40:48],line[48:56]))
        # Decrease id -1 due to fortran notation
        points = [ p-1 for p in points]
        geometry['QUAD'].append(points)

nGeometryPoints = len(geometry['GRID'])
nGeometryTrias = len(geometry['TRIA'])
nGeometryQuads = len(geometry['QUAD'])

print 'Finished geometry.'

print 'Extracted from file:'
print '\tpoints {0}'.format(len(geometry['GRID']))
print '\ttrias  {0}'.format(len(geometry['TRIA']))
print '\tquads  {0}'.format(len(geometry['QUAD']))

print '\nReading modes.'
modeNo = -1
while 1:
    try:
        line=modesPtr.next()
        if line[1:11] == 'EIGENVALUE':
            modeNo = int(line.split()[5])
            shapes[modeNo] = []
            line = modesPtr.next()
        if modeNo != -1:
            try:
                v0 = map(float, line.split()[2:5])
                line = modesPtr.next()
                v1 = map(float, line.split()[1:4])
                #shapes[modeNo].append((v0,v1))
                shapes[modeNo].append(v0)
            except:
                continue
    except:
        print 'EOF', modeFileNAme
        break

print 'Read {0} modes'.format(modeNo)

print 'Min and max length of mode data set\n(should be equal and equal to points above):'
minlen = 1e9
maxlen = 0
for a in shapes.values():
    minlen = min(minlen, len(a))
    maxlen = max(maxlen, len(a))

print 'Min length = {0}'.format(minlen)
print 'Max length = {0}'.format(maxlen)

# Export to VTK poly data format

import vtk
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

# Add mode data
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



polyData.Modified()

writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName('data.vtp')
writer.SetInputData(polyData)
writer.Write()

#writer = vtk.vtkXMLUnstructuredGridWriter()
#writer.SetDataModeToAscii()
#writer.SetFileName('data.xml')
#writer.SetInputData(points)
#writer.Write()

