#!/usr/bin/env python

import os,sys,re,string
from struct import *
from types import *
from numpy import array


def getArgs():
    from optparse import OptionParser
    descString = """
    Python thing to scale obj file vertices
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--file',dest='objFile',default=None,help='Input obj file')
    parser.add_option('-o','--output',dest='output',default=None,help='Output obj file')
    parser.add_option('-s','--scale',dest='scale',default=1.0,help='Scaling factor')
    parser.add_option('-B','--boundingbox',dest='bounds',action='store_true',default=False,help='Calculate bounding box')
    parser.add_option('-t','--split',dest='split',action='store_true',default=False,help='Split into separate files')
    parser.add_option('-b','--binary',dest='binary',action='store_true',default=False,help='NOT IMPLEMENTED. Input file is binary')
    parser.add_option('-T','--translate',dest='translate',default=None,help='Translate all vertices')

    (opt,arg)=parser.parse_args()

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)

    if not opt.objFile: argError( 'Missing obj file argument' )
    objIn = opt.objFile
    objBase = os.path.splitext(objIn)[0]
    objExt = os.path.splitext(objIn)[1]
    objOut = opt.output
    if not opt.output:
        objOut = objBase+'_scaled'+objExt
    translation=[0,0,0]
    if opt.translate:
        tString = opt.translate
        try:
            translation = map(float,opt.translate.strip('()').split())
        except:
            argError('translation vector not in format \"(x y z)\".')



    return opt,arg


class objToolBox:
    def __init__(self,objFile,objOutFile):
        self.objFile = objFile
        self.objHandle = open(objFile)
        self.regions = []
        self.objOut = objOutFile
        self.head = ''
        self.verts = []
        self.data = None
        self.faces = {}
        self.read()
        self.getVerts()

    def extractRegionName(self,line):
        return line.split(' ',1)[1]

    def action(self, scale=1.0, split=False, bounds=False, translate=False):
        if sum(map(abs,translate)) > 0:
            self.translate(translate)
            sys.exit(0)
        if bounds:
            self.calcBounds()
            sys.exit(0)
        if scale != 1.0:
            self.scale(scale)
            sys.exit(0)
        if split:
            self.split()
            sys.exit(0)

    def read(self):
        ''' Store all non-empty lines
        and strip whites and newls'''
        self.data = [
                        line for line in 
                        map(string.strip, self.objHandle.readlines()) 
                        if line
                    ]

    def getHead(self):
        '''Reading file header.
        Assuming first non header line is a vertex'''
        for line in self.data:
            if line[0] == 'v':
                break
            self.head += '{0}\n'.format(line) if line else '#'

    def getVerts(self):
        print 'Reading obj vertices'
        for line in self.data:
            if line[0] == 'g':
                break
            if line and line[0] == 'v':
                v = array(map(float,line.split()[-3:]))
                self.verts.append(v)

    def getFaces(self):
        regionName = 'defaultRegion'
        for line in self.data:
            if line[0] == 'g':
                regionName = self.extractRegionName(line)
                self.faces[regionName] = []
            if line[0] == 'f':
                f = map(int,line.split()[1:])
                self.faces[regionName].append(f)

    def getRegionFaces(self,region='defaultRegion'):
        if not self.faces:
            self.getFaces()
        if self.faces.has_key(region):
            return self.faces[region]
        else:
            print 'Cannot find region', region, 'in data'
            return []

    def getRegionVerts(self,region=''):
        '''Return a generator for selected vertices.
        Returns all vertices if not region set.'''
        def f(faces):
            vertInds = []
            for face in faces:
                vertInds+=face
            vertInds = set(vertInds)

            for v in vertInds:
                yield self.verts[v-1]

        if region:
            faces = self.getRegionFaces(region)
            return f(faces)
        else:
            return (v for v in self.verts)

    def vertsStr(self):
        return ( 'v {0:e} {1:e} {2:e}\n'.format(v) for v in self.verts )

    def translate(self,translation):
        print 'Translating obj vertices by vector',translation
        def f(v,t):
            t = array(t)
            return [ a+t for a in v ]
        self.verts = f(self.verts,translation)

    def scale(self,scaleFactor):
        print 'Scaling obj vertices by factor',scaleFactor
        def f(v,s):
            return [ a*s for a in v ]
        self.verts = f(self.verts,scaleFactor)

    def calcBounds(self, region='defaultRegion'):
        print '\tCalculating bounding box for', self.objFile
        minX=minY=minZ =  1.0e10
        maxX=maxY=maxZ = -1.0e10
        verts = []

        cX=cY=cZ=0.0
        for v in self.getRegionVerts(region):
            X,Y,Z = v
            minX,minY,minZ = min(minX,X),min(minY,Y),min(minZ,Z)
            maxX,maxY,maxZ = max(maxX,X),max(maxY,Y),max(maxZ,Z)
            cX,cY,cZ=[(maxX+minX)/2.,(maxY+minY)/2.,(maxZ+minZ)/2.]

        print '''\tobj bounds for %s in %s =
        centre (%f, %f, %f)
        min    (%f, %f, %f)
        max    (%f, %f, %f)
        size   (%f, %f, %f)
        ''' % (region,self.objFile,cX,cY,cZ,minX,minY,minZ,maxX,maxY,maxZ,maxX-minX,maxY-minY,maxZ-minZ)

        return (minX,minY,minZ),(maxX,maxY,maxZ)

    def split(self):
        print 'Spliting obj file into regions:'
        pass

    def getRegions(self):
        for line in self.data:
            if line[0] == 'g':
                self.regions.append(self.extractRegionName(line))


if __name__=='__main__':
    options, arguments = getArgs()

    ot = objToolBox(options.objFile, options.output)

    ot.getHead()
    print ot.head

    ot.scale(1.0)
    ot.translate([0,0,0])
    ot.getRegions()

    print 'Containing regions:'
    for r in ot.regions:
        ot.calcBounds(r)

    #for line in ot.vertsStr():
    #    print line
