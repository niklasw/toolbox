#!/usr/bin/env python

import re, sys, os, fileinput

def cleanString(str):
     return re.sub(r'\s','',str,re.DOTALL)

def zipup(file):
     cmd = 'gunzip -r '+file
     os.popen(cmd)

def zip(file):
     cmd = 'gzip -r '+file
     os.popen(cmd)

class foamFieldObjectReader:
     def __init__(self,file):
          self.nPattern = re.compile(r'^\s*\d+\s*(\/\/)*\s*$')
          self.cellShapePattern = re.compile\
               (r'^\s*\(\s*\d+\s+\d\s*\(\s*(\d+\s+)+\d+\s*\)\s*\)\s*$')
          self.vectorPattern = re.compile\
               (r'^\s*\((\s*[-]?\d+(\.\d*)?([Ee][+-]\d+)?){3,3}\s*\)\s*$')
          self.scalarPattern = re.compile\
               (r'^\s*[+-]*\d+\s*\.?\d*[eE][+-]\d*$')
          self.classPattern = re.compile(r'^\s*(class)\s+\w+\s*;\s*$')
          self.patterns = {'shapeList':self.cellShapePattern,\
                           'vectorField':self.vectorPattern,\
                           'scalarField':self.scalarPattern,\
                           'volScalarField':self.scalarPattern}
          self.file = file
          self.objectType = ''
          self.zipped = 0
          if os.path.isfile(self.file+'.gz') and \
                 not os.path.isfile(self.file):
               self.file = self.file+'.gz'
               self.zipped = 1

          if self.zipped:
               zipup(file)
               self.file = self.file[0:-3]

     def close(self):
          if self.zipped:
               zip(self.file)
          return

     def getObjectType(self):
          fh = open(self.file,'r')
          line = 'XXXXX'
          items = []
          while line:
               line = fh.readline()
               if self.classPattern.search(line):
                    line = line.split()[1]
                    line = re.sub(r'[;]','',line)
                    self.objectType = line.strip()
                    fh.close()
                    return
          print "OBJECT TYPE IN "+self.file+" NOT FOUND, EXITING"
          fh.close()
          sys.exit()

     def getCellShapeInfo(self,shape):
          shape = re.sub('\(','',shape,1)
          tmp = shape.split(' ',1)
          typeId = tmp[0]
          nPoints =  tmp[1].split('(',1)[0]
          return typeId,nPoints

     def read(self):
          pat = self.patterns[self.objectType]
          nitems = 0
          items = []
          for line in fileinput.input(self.file):
               if self.nPattern.search(line) and nitems == 0:
                    nitems = int(line.strip())
               if pat.search(line):
                    items.append(line.strip())
          if nitems == 0 or len(items) != nitems:
               print "ERROR ",nitems,len(items)
               print "READ ERROR in read()"
               self.close()
               sys.exit()
          print '...done'
          return nitems,items



path = sys.argv[1]
meshPath = path+'/constant/polyMesh'
instant = path+'/0.064'
scalarField = instant+'/p'
vectorField = instant+'/u'

pointReader = foamFieldObjectReader (meshPath+'/points')
pointReader.getObjectType ()
print pointReader.objectType
npoints,points = pointReader.read()
for item in points:
     pass
     #print item

cellReader = foamFieldObjectReader (meshPath+'/cellShapes')
cellReader.getObjectType ()
print cellReader.objectType
n,cells =  cellReader.read ()
for item in cells:
     pass
     #print cellReader.getCellShapeInfo(item)

fieldReader = foamFieldObjectReader (scalarField)
fieldReader.getObjectType()

n,scalars = fieldReader.read()
print n
for item in scalars:
     print item

