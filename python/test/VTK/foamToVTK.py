#!/usr/bin/env python

import re,sys,os

def getArgs():
    return sys.argv

def init(argList):
    args = getArgs()
    root,case = args[1], args[2]
    meshDir = "/constant/polyMesh"
    casePath = root+"/"+case
    meshPath = casePath+meshDir
    points = meshPath+"/points"
    cells = meshPath+"/cellShapes"
    faces = meshPath+"/faces"
    vtkFile = casePath+"/VTKdata.vtk"
    return {'root':root,'case':case,\
            'casePath':casePath,\
            'meshPath':meshPath,\
            'cells':cells,'points':points,'faces':faces,\
            'vtkFile':vtkFile}

def readFile(file):
    f = open(file,'r')
    linesAll = f.read()
    f.close()
    return linesAll

def removeCppComments(str):
    pat1 = re.compile(r'/\*(.*)\*/',re.DOTALL)
    pat2 = re.compile(r'//(.*)\n')
    str = pat1.sub('',str)
    str = pat2.sub('',str)
    return str

def removeHeader(str):
    pat = re.compile(r'(FoamFile)(.*)}',re.DOTALL)
    return pat.sub('',str)

def removeParens(str):
    pat = re.compile(r'[\(|\)]')
    return pat.sub(' ',str)

def removeEmptyListItems(alist):
    return filter(None,alist)

def cleanMeshString(str):
    return removeHeader \
           (removeParens \
           (removeCppComments (str)))

def stringToList(str,sep='\n'):
    return removeEmptyListItems(str.split(sep))

def getCleanData(File):
    Str = cleanMeshString (readFile (File))
    return stringToList(Str)

def countItems(slist):
    n=0
    for item in slist:
        n+=len(item.split()[1:])
    return n     

def vtkHeader():
    return "# vtk DataFile Version 2.0\nUnstructured Grid\nASCII"\
    +"\nDATASET UNSTRUCTURED_GRID\n\n"

def writePoints(fh,plist):
    fh.write('POINTS '+plist[0]+' float\n')
    for point in plist[2:]:
        fh.write(point+'\n')
    fh.write('\n')        
    return

def writeCells(fh,clist):
    fh.write('CELLS '+clist[0]+' '+str(countItems(clist[2:]))+'\n')
    cellTypes = []
    for cell in clist[2:-1]:
        cell = cell.split()        
        cellTypes.append(cell[0])
        [ fh.write(cell[i]+' ') for i in range(1,len(cell)) ]
        fh.write('\n')
    fh.write('\n')
    cellTypeConversion ={'3':'12'}
    fh.write('CELL_TYPES '+clist[0]+'\n')    
    for Type in cellTypes:
        fh.write (cellTypeConversion[Type]+'\n')
    fh.write('\n')
    return

def writeSampleData(fh,plist):
    fh.write('POINT_DATA '+plist[0]+'\nSCALARS pointScalar float\nLOOKUP_TABLE default\n')
    i=0
    for point in plist[2:]:
        i+=1
        fh.write(str(i)+'.0\n')
    fh.write('\n')    
    return

def writeSampleCellData(fh,clist):
    fh.write('CELL_DATA '+clist[0]+'\nSCALARS scalars float\nLOOKUP_TABLE default\n')
    i=0
    for point in clist[2:]:
        i+=1
        fh.write(str(i)+'\n')
    fh.write('\n')    
    return

def main():
    arglist = getArgs()
    paths = init(getArgs())

    pointsFile = paths['points']
    cellsFile = paths['cells']
    outFile = paths['vtkFile']

    pointsL = getCleanData(pointsFile)
    cellsL = getCleanData(cellsFile)

    vtkf = open (outFile,'w')
    vtkf.write(vtkHeader())
    writePoints(vtkf,pointsL)
    writeCells(vtkf,cellsL)
#    writeSampleCellData(vtkf,cellsL)
    writeSampleData(vtkf,pointsL)
    print 'DONE'
        
main()
    
    
    
