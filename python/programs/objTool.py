#!/usr/bin/env python

import os,sys,re,string
from numpy import array


def getArgs():
    from optparse import OptionParser
    descString = """
    Python thing to scale obj file vertices
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--file',dest='objFile',default=None,help='Input obj file')
    parser.add_option('-a','--append',dest='append',default=None,help='obj file to append')
    parser.add_option('-o','--output',dest='output',default=None,help='Output obj file')
    parser.add_option('-s','--scale',dest='scale',default=None,help='Scaling factor')
    parser.add_option('-t','--translate',dest='translate',default=None,help='Translate all vertices')
    parser.add_option('-B','--boundingbox',dest='bounds',action='store_true',default=False,help='Calculate bounding box')
    parser.add_option('-T','--split',dest='split',action='store_true',default=False,help='Split into separate files')
    parser.add_option('-b','--binary',dest='binary',action='store_true',default=False,help='NOT IMPLEMENTED. Input file is binary')

    (opt,arg)=parser.parse_args()

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print('\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*'))
        parser.print_help()
        sys.exit(1)

    if not opt.objFile: argError( 'Missing obj file argument' )
    objIn = opt.objFile
    objBase = os.path.splitext(objIn)[0]
    objExt = os.path.splitext(objIn)[1]
    objOut = opt.output
    if not opt.output:
        objOut = objBase+'_new'+objExt
    opt.output = objOut

    if opt.scale:
        try:
            opt.scale = float(opt.scale)
        except:
            argError('translation vector not in format \"(x y z)\".')

    if opt.translate:
        try:
            opt.translate = list(map(float,opt.translate.strip('()').split()))
        except:
            argError('translation vector not in format \"(x y z)\".')

    if opt.append:
        if not os.path.isfile(opt.append):
            argError('Cannot read obj file to append')
        else:
            print('Will append {} to {}, writing to {}'.format(opt.append,opt.objFile,opt.output))

    return opt,arg

class vertex:
    def __init__(self,v=(1e10,1e10,1e10)):
        self.v = array(v)

    def __str__(self):
        return 'v {0:e} {1:e} {2:e}\n'.format(*self.v)

    def fromLine(self,line):
        self.v = array(list(map(float,line.split()[-3:])))

    def translate(self,t):
        self.v += array(t)
    def scale(self,s):
        self.v *= array(s)

class face:
    def __init__(self,i=[]):
        self.indices = i

    def shiftVerts(self,offset):
        self.indices = [i+offset for i in self.indices]
        return self

    def __str__(self):
        fmt = 'f'+' {:d}'*len(self.indices)+'\n'
        return fmt.format(*self.indices)

class objToolBox:
    def __init__(self,objFile,objOutFile='default.obj',binary=False):
        self.objFile = objFile
        self.objHandle = open(objFile)
        self.regions = [] # List of names
        self.objOut = objOutFile
        self.head = ''
        self.verts = []
        self.data = None
        self.faces = {}
        self.read()
        self.getVerts()
        self.getRegions()
        self.ops = {'scale': lambda v,s: v.scale(s),
                    'translate': lambda v,t: v.translate(t),
                    'append': lambda v,a: v.append(a)}

    def extractRegionName(self,line):
        return line.split(' ',1)[1]

    def read(self):
        ''' Store all non-empty lines
        and strip whites and newls'''
        self.data = [
                        line for line in 
                        map(str.strip, self.objHandle.readlines()) 
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
        print('Reading obj vertices')
        for line in self.data:
            if line and line[0] == 'v' and line[1] != 'n':
                try:
                    v = vertex()
                    v.fromLine(line)
                    self.verts.append(v)
                except:
                    print("Error reading vertex")
                    sys.exit(1)
                    

    def getFaces(self):
        regionName = 'defaultRegion'
        slashPat = re.compile(r'\/\/[0-9]+')
        spacePat = re.compile(r'\s+')
        for line in self.data:
            if line[0] == 'g':
                regionName = self.extractRegionName(line)
                self.faces[regionName] = []
            if line[0] == 'f':
                if '/' in line: # Some obj writers make f 22//22 ...
                    labels = [int(a) for a in slashPat.split(line) if a.isdigit()]
                else:
                    labels = [int(a) for a in spacePat.split(line) if a.isdigit()]

                f = face(labels)
                self.faces[regionName].append(f)

    def getRegionFaces(self,region='defaultRegion'):
        if not self.faces:
            self.getFaces()
        if region in self.faces:
            return self.faces[region]
        else:
            print('Cannot find region', region, 'in data')
            return []

    def getRegionVerts(self,region=''):
        '''Return a generator for selected vertices.
        Returns all vertices if not region set.'''
        def F(faces):
            vertInds = []
            for f in faces:
                vertInds+=f.indices
            vertInds = set(vertInds)

            for v in vertInds:
                yield self.verts[v-1]

        if region:
            faces = self.getRegionFaces(region)
            return F(faces)
        else:
            return (v for v in self.verts)

    def vertsStr(self):
        return ( vertex(v).__str__() for v in self.verts )

    def writeRegion(self,regionName):
        for v in self.getRegionVerts(regionName):
            print(v)


    def bounds(self, region=''):
        minX=minY=minZ =  1.0e10
        maxX=maxY=maxZ = -1.0e10
        verts = []

        cX=cY=cZ=0.0
        for vert in self.getRegionVerts(region):
            X,Y,Z = vert.v
            minX,minY,minZ = min(minX,X),min(minY,Y),min(minZ,Z)
            maxX,maxY,maxZ = max(maxX,X),max(maxY,Y),max(maxZ,Z)
            cX,cY,cZ=[(maxX+minX)/2.,(maxY+minY)/2.,(maxZ+minZ)/2.]

        print('''\tBounds for %s =
        centre (%f, %f, %f)
        min    (%f, %f, %f)
        max    (%f, %f, %f)
        size   (%f, %f, %f)
        ''' % (region,cX,cY,cZ,minX,minY,minZ,maxX,maxY,maxZ,maxX-minX,maxY-minY,maxZ-minZ))

        return (minX,minY,minZ),(maxX,maxY,maxZ)

    def extractRegions(self,regionsToExtract):
        for region in regionsToExtract:
            if not self.faces:
                self.getFaces()
                if not region in list(self.faces.keys()):
                    print('Cannot find region {0} in geometry'.format(region))
                    sys.exit(1)
                else:
                    regionFaces = self.faces[region]
                    pass

    def split(self):
        print('Spliting obj file into regions:')
        print('\t!NOT IMPLEMENTED')
        pass

    def transform(self,op,v):
        [ op(a,v) for a in self.verts ]

    def getRegions(self):
        for line in self.data:
            if line[0] == 'g':
                self.regions.append(self.extractRegionName(line))

    def write(self):
        with open(self.objOut,'w') as fp:
            for r in self.regions:
                for v in self.getRegionVerts(r):
                    fp.write(v.__str__())
                fp.write('g {0}\n'.format(r))
                for f in self.getRegionFaces(r):
                    fp.write(f.__str__())

    def append(self,ot2):
        indexOffset = len(self.verts)
        self.verts += ot2.verts
        for r in ot2.regions:
            self.regions.append(r)
            self.faces[r] = [f.shiftVerts(indexOffset) for f in ot2.faces[r]]

def test1():
    options, arguments = getArgs()

    ot = objToolBox(options.objFile, options.output)

    if options.translate:
        ot.transform(ot.ops['translate'], options.translate)
    if options.scale:
        ot.transform(ot.ops['scale'], options.scale)
    if options.append:
        ot2 = objToolBox(options.append)
        ot.getFaces()
        ot2.getFaces()
        ot.append(ot2)

    print('Per region bounding box. NOT IMPLEMENTED')
    #for r in ot.regions:
    #    if options.bounds:
    #        ot.bounds(region=r)

    print('Overall bounding box')
    ot.bounds(region='')
    ot.write()

def testAppend():
    f1=sys.argv[1]
    f2=sys.argv[2]
    ot1 = objToolBox(f1,'merged.obj')
    ot2 = objToolBox(f2,'dummy.obj')
    ot1.getFaces()
    ot2.getFaces()
    ot1.append(ot2)
    ot1.write()

if __name__=='__main__':
    test1()
