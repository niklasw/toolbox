#!BPY

"""
Name: 'BlockMesh Exporter GUI'
Blender: 244
Group: 'Export'
Tooltip: 'Export selected orthogonal hex blender mesh to blockMesh format '
"""
__author__ = "Niklas Wikstrom"
__url__ = ("")
__version__ = "1.0 2008-12-28"

__bpydoc__ = """\
This script helps in the generation of a blockMeshDict file for OpenFOAM
"""

# --------------------------------------------------------------------------
# blockMeshExporterGUI.py
# Program versions: Blender 2.45+ 
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2008: Niklas Wikstrom
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
# --------------------------------------------------------------------------

import Blender, os
from Blender.Mathutils import Vector

def l2s(alist):
    import re
    return '(%s)' % re.sub(',','',str(alist))[1:-1]

class Coord(list):
    def __init__(self,coord=[0,0,0]):
        list.__init__(self,coord)
        self.x = float(coord[0])
        self.y = float(coord[1])
        self.z = float(coord[2])
        self.coord = coord
    def __str__(self):
        return '(%f %f %f)' % (self.x,self.y,self.z)

class Node(Coord):
    def __init__(self, coords=[0,0,0], index=-1):
        Coord.__init__(self,coords)
        self.index = index
    def __str__(self):
        return '(%f %f %f) // %i' % (self.x, self.y, self.z, self.index)

class NodeList(list):
    def __init__(self,l=[]):
        list.__init__(self,l)

    def __str__(self):
        s = 'vertices\n(\n'
        for item in self:
            s += '    '+str(item)+'\n'
        s += ');\n'
        return s

    def indices(self):
        return [ n.index for n in self ]

    def coords(self):
        return [n.coord for n in self]

    def sorted(self,dir,rev=False):
        import operator
        return NodeList(sorted(self,key=operator.attrgetter(dir), reverse=rev))

    def read(self,BM):
        import re
        fp = open(BM.fileName,'r')
        listStart = re.compile('^\s*vertices\s*$')
        listEnd = re.compile('^\s*\)\s*;')
        vertexPat = re.compile('^\s*\((\s*.+\s+.+\s+.+\s*)\).*$')
        line = 'x'
        while line:
            line = fp.readline()
            if listStart.match(line):
                break
        while line:
            line = fp.readline()
            match = vertexPat.match(line)
            if match:
                coord = map(float,match.group(1).split())
                self.append(Node(coord,len(self)))
            elif listEnd.match(line):
                print line
                break
        print self

class Block:
    def __init__(self, nodes=NodeList(), resol = (1,1,1), grading = (1,1,1)):
        self.nodes = nodes
        self.res = list(resol)
        self.grading = list(grading)
        self.OK = False

    def __str__(self):
        str = 'hex %s %s simpleGrading %s'% (l2s(self.nodes.indices()), l2s(self.res), l2s(self.grading))
        return str

    def assertHex(self,BM): # blockMaker() as argument for communication purpose only
        if len(self.nodes) != 8:
            self.OK = False
            BM.error('Not 8 points selected')
            BM.OK = False
        else:
            self.OK = True
            BM.info('8 points selected OK')
            BM.OK = True

    def cartesianSort(self,BM): # blockMaker() as argument for communication purpose only
        self.assertHex(BM)
        if self.OK:
            n = self.nodes.sorted('z')
            n[0:4] = NodeList(n[0:4]).sorted('y')
            n[0:2] = NodeList(n[0:2]).sorted('x')
            n[2:4] = NodeList(n[2:4]).sorted('x', rev=True)
            n[4:8] = NodeList(n[4:8]).sorted('y')
            n[4:6] = NodeList(n[4:6]).sorted('x')
            n[6:8] = NodeList(n[6:8]).sorted('x', rev=True)
            self.nodes = n
            return True
        else:
            print self.nodes
            return False

    def filedBlockPattern(self):
        import re
        pat=re.compile('^ *hex *\(([0-9]+.*?)\)\s*\(([0-9]+.*?)\).*\(([0-9]+.*:?)\)$')
        return pat

    def neighbours(self,allBlocks):
        testMasks = {'xmin':[1,0,0,1,1,0,0,1],
                     'xmax':[0,1,1,0,0,1,1,0],
                     'ymin':[1,1,0,0,1,1,0,0],
                     'ymax':[0,0,1,1,0,0,1,1],
                     'zmin':[1,1,1,1,0,0,0,0],
                     'zmax':[0,0,0,0,1,1,1,1]}

        neighbours = {}
        if len(allBlocks) > 1:
            for other in allBlocks:
                mask = [ i in other.nodes.indices() for i in self.nodes.indices()]
                nCommon = mask.count(True)
                if nCommon == 4:
                    for key in testMasks:
                        if mask == testMasks[key]:
                            neighbours[key] = other
        return neighbours

    def copyFromNeighbours(self,allBlocks):
        nbrs = self.neighbours(allBlocks)
        for key in nbrs:
            if key == 'xmin' or key == 'xmax':
                self.res[1] = nbrs[key].res[1]
                self.res[2] = nbrs[key].res[2]
            elif key == 'ymin' or key == 'ymax':
                self.res[0] = nbrs[key].res[0]
                self.res[2] = nbrs[key].res[2]
            elif key == 'zmin' or key == 'zmax':
                self.res[0] = nbrs[key].res[0]
                self.res[1] = nbrs[key].res[1]

    def copyToNeighbours(self,allBlocks):
        nbrs = self.neighbours(allBlocks)
        for key in nbrs:
            if key == 'xmin' or key == 'xmax':
                nbrs[key].res[1] = self.res[1]
                nbrs[key].res[2] = self.res[2]
            elif key == 'ymin' or key == 'ymax':
                nbrs[key].res[0] = self.res[0]
                nbrs[key].res[2] = self.res[2]
            elif key == 'zmin' or key == 'zmax':
                nbrs[key].res[0] = self.res[0]
                nbrs[key].res[1] = self.res[1]



class BlockList(list):
    def __init__(self,l=[]):
        list.__init__(self,l)

    def __str__(self):
        s = '\nblocks\n(\n'
        for block in self:
            s += '    '+str(block)+'\n'
        s += '\n);\n'
        return s

    def nodeIndices(self):
        return [ b.nodes.indices() for b in self ]

    def index(self):
        return [ b.index for b in self ]

    def appendBlock(self,block):
        if not block.nodes.indices() in self.nodeIndices():
            self.append(block)
            return len(self)-1
        else:
            return self.nodeIndices().index(block.nodes.indices())

    def read(self, BM):
        """This function needs a node list to be present in blockMaker BM!
           Also one complete block definition per line in file!"""
        #BM.collectPoints()
        if not os.path.isfile(BM.fileName):
            BM.info('File blockMeshDict not found:'+BM.fileName)
            return False
        fp = open(BM.fileName,'r')
        blockDefs = [] 
        for line in fp:
            match = Block().filedBlockPattern().match(line)
            if match:
                blockDefs.append(match.group(1,2,3))
        for blockDef in blockDefs:
            indices = map(int,blockDef[0].split())
            nodes = NodeList()
            print 'BlockList.read() BM.allNodes',BM.allNodes
            for idx in indices:
                try:
                    nodes.append(Node(BM.allNodes[idx], idx))
                except:
                    BM.error('Block node index %i out of range!' % idx)
            print nodes
            res   = map(int,blockDef[1].split())
            grad  = map(float,blockDef[2].split())
            if BM.OK:
                self.appendBlock(Block(nodes=nodes, resol=res, grading=grad))
            else:
                BM.error('Warning: Blocks not appended. Some error.')

class MeshManipulator:
    """Note that here verts is blender points"""
    def __init__(self,new=False):
        import bpy
        in_editmode = Blender.Window.EditMode()
        if in_editmode: Blender.Window.EditMode(0)
        objects = Blender.Object.GetSelected()
        scn = bpy.data.scenes.active
        if objects:
            self.ob = objects[0]
            self.me = self.ob.getData(mesh=1)
        elif new:
            self.me = bpy.data.meshes.new(name='newMesh')
            self.ob = scn.objects.new(self.me, 'newObj')
            print 'New mesh object in target?'
        else:
            self.me = bpy.data.meshes.new(name='noMesh')
            self.ob = scn.objects.new(self.me, 'noObj')
            self.error = 'Could not select mesh'
            self.OK = False
        self.ve = self.me.verts
        self.OK = True
        if in_editmode: Blender.Window.EditMode(1)

    def editMode(self, set):
        Blender.Window.EditMode(set)

    def removeDoubles(self):
        in_editmode = Blender.Window.EditMode()
        if in_editmode:
            Blender.Window.EditMode(0)
        for v in self.ve:
            v.sel = 1
        nRemoved = self.me.remDoubles(0.0001)
        if in_editmode:
            Blender.Window.EditMode(1)
        return nRemoved

    def selectedVerts(self, selected=1):
        return [ v for v in self.ve if v.sel == selected ]

    def unselectAll(self):
        in_editmode = Blender.Window.EditMode()
        if in_editmode:
            Blender.Window.EditMode(0)
        for v in self.ve:
            v.sel = 0
        if in_editmode:
            Blender.Window.EditMode(1)

    def facetNormal(self):
        v= self.selectedVerts()
        normal = Vector(0,0,0)
        if len(v) == 3:
            v0 = Vector(v[0].co*self.ob.matrix)
            v1 = Vector(v[1].co*self.ob.matrix)
            v2 = Vector(v[2].co*self.ob.matrix)
            normal = Blender.Mathutils.TriangleNormal(v0,v1,v2)
        else:
            self.error = 'Not 3 vertices selceted'
            self.OK = False
        return normal

    def createNewBlock(self,block):
        import bpy,operator
        from operator import itemgetter
        self.editMode(0)
        coords = block.nodes.coords()
        self.me.verts.extend(coords)
        indices = block.nodes.indices()
        print indices
        fac = []
        fac.append(list(itemgetter(0,1,2,3)(indices)))
        fac.append(list(itemgetter(4,5,6,7)(indices)))
        fac.append(list(itemgetter(0,1,5,4)(indices)))
        fac.append(list(itemgetter(0,4,7,3)(indices)))
        fac.append(list(itemgetter(3,2,6,7)(indices)))
        fac.append(list(itemgetter(1,2,6,5)(indices)))
        print fac
        self.me.faces.extend(fac)
        scn = bpy.data.scenes.active


class blockMaker:
    def __init__(self):
        self.allNodes = NodeList([])
        self.selNodes = NodeList([])
        self.blocks = BlockList([])
        self.fileName = '/tmp/blockMeshDict'
        self.OK = True
        self.message = ''
        self.currentBlockIndex = -1
        self.currentBlock = Block()

    def clear(self):
        self.info('Clear all')
        self.allNodes = NodeList([])
        self.selNodes = NodeList([])
        self.blocks = BlockList([])
        self.OK = True
        self.currentBlockIndex = -1
        self.currentBlock = Block()
        self.info('Block list is now empty')
        print self.blocks
        print self.allNodes

    def info(self,astring):
        self.message  = '\nInfo: ' + astring
        print '*** '+astring

    def error(self,astring):
        self.message = 'Error: ' + astring
        self.OK = False
        print '!** '+astring

    def removeDoubles(self):
        n = MeshManipulator().removeDoubles()
        self.info('Removed %i vertices' % n)

    def collectPoints(self):
        """ a point is here a tuple of (x, y, z, index)
        All points should be transformed to global coordinates!"""
        MM = MeshManipulator()
        self.allNodes = NodeList([ Node(v.co*MM.ob.matrix, v.index) for v in MM.ve ])
        self.selNodes = NodeList([ Node(v.co*MM.ob.matrix, v.index) for v in MM.selectedVerts() ])
        self.info('%i points collected' % len(self.selNodes))
        return MM

    def readPoints(self):
        self.allNodes.read(self)

    def collectBlock(self, unselect=False):
        MM = self.collectPoints()
        tBlock = Block(nodes=self.selNodes)
        if tBlock.cartesianSort(self):
            print tBlock.nodes
            self.currentBlockIndex = self.blocks.appendBlock(tBlock)
            self.currentBlock = self.blocks[self.currentBlockIndex]
            self.currentBlock.neighbours(self.blocks)
            self.info('Block id = %i (# registred blocks =%i)' % (self.currentBlockIndex, len(self.blocks)))
            print self.currentBlock
            if unselect:
                MM.unselectAll()

    def removeBlock(self):
        self.blocks.remove(self.currentBlock)
        print self.currentBlockIndex
        print self.blocks, len(self.blocks)
        self.currentBlockIndex -=1
        self.currentBlock = self.blocks[self.currentBlockIndex]
        self.currentBlock.neighbours(self.blocks)
        self.info('Block id = %i (# registred blocks =%i)' % (self.currentBlockIndex, len(self.blocks)))

    def readBlocks(self):
        self.clear()
        self.readPoints()
        blockList = BlockList()
        blockList.read(self)
        print blockList
        MM = MeshManipulator(new=True)
        for block in blockList:
            print block
            MM.createNewBlock(block)
        self.insertBlockList(blockList)

    def insertBlockList(self,blocks=[]):
        for block in blocks:
            self.currentBlockIndex = self.blocks.appendBlock(block)
            self.currentBlock = self.blocks[self.currentBlockIndex]
        self.info('Block id = %i (# registred blocks =%i)' % (self.currentBlockIndex, len(self.blocks)))

    def selectByIndex(self, index):
        if self.blocks:
            # if index exceeds block list size-1 select last
            index = min(len(self.blocks)-1,index)
            self.currentBlockIndex = index
            self.currentBlock = self.blocks[index]
            self.info('Block id = %i (# registred blocks =%i)' % (self.currentBlockIndex, len(self.blocks)))
        else:
            self.info('No blocks currently registered')

    def showBlock(self, show=True):
        pos = Blender.Mathutils.Vector((0,0,0))
        if self.blocks:
            MM = MeshManipulator()
            MM.editMode(0)
            for v in MM.ve:
                if v.index in self.currentBlock.nodes.indices():
                    pos += v.co*MM.ob.matrix
            if show:
                for v in MM.ve:
                    v.sel = 0
                    if v.index in self.currentBlock.nodes.indices():
                        v.sel = 1
            MM.editMode(1)
            pos /= len(self.currentBlock.nodes)
            Blender.Window.SetCursorPos(pos)

    def patchesAndStuff(self):
        str = '\nedges ();\npatches ();\nmergePatchPairs ();\n'
        return str

    def writeDict(self, pointSelection='all', writeBlock=True,final=False):
        self.info('Will create new file'+self.fileName)
        self.collectPoints()
        out = open(self.fileName, 'w')
        out.write(self.head())
        if pointSelection == 'all':
            print self.allNodes
            out.write(str(self.allNodes))
        else:
            print self.selNodes
            out.write(str(self.selNodes))
        if writeBlock:
            print self.blocks
            out.write(str(self.blocks))
        if final:
            out.write(self.patchesAndStuff())
        out.close()

    def head(self):
        return '''
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

convertToMeters 1;

'''

    def writeRestOfFile(self):
        str = '\nedges ();\npatches ();\nmergePatchPairs ();\n'
        out = open(self.fileName,'a')
        out.write(str)

# - - - - - - - - - - - - - - - - - - - - 

exportFileName = '/tmp/blockMeshDict'
blockEngine = blockMaker()
copyResX = copyResY = copyResZ = 0

resX = Blender.Draw.Create(1)
resY = Blender.Draw.Create(1)
resZ = Blender.Draw.Create(1)

def gui():     
    global blockEngine
    global blockIndex
    global resX, resY, resZ
    global copyResX, copyResY, copyResZ
    x0=  10
    x = lambda d: d*96 + x0
    y = lambda d: d*20
    w= lambda d: d*96
    h= lambda d: d*20
    blockEngine.fileName = exportFileName
    Blender.BGL.glClear(Blender.BGL.GL_COLOR_BUFFER_BIT) 
    Blender.BGL.glRasterPos2d(               x0+x(2),  y(7))
    Blender.Draw.Text(blockEngine.message)
    Blender.Draw.Button(exportFileName,     1,  x(0),  y(8), w(2), h(1), 'File selector opens')
    Blender.Draw.Button('Read blocks',       35,  x(2),  y(8), w(1), h(1), 'Read block defs from file')
    Blender.Draw.Button('Read points',       36,  x(3),  y(8), w(1), h(1), 'Read block defs from file')
    Blender.Draw.Button('Write points only',6,  x(0),  y(7), w(2), h(1), 'Write selected points only. Overwrites!')
    Blender.Draw.Button('Remove doubles',  16,  x(0),  y(6), w(2), h(1), 'Remove all double vertices')
    Blender.Draw.Button('Register block',   7,  x(0),  y(5), w(1), h(1), 'Collect selected points to for one block')
    Blender.Draw.Toggle('X',               11,  x(1),  y(5), w(1)/3, h(1), copyResX, 'Copy X resolution from current (last) block')
    Blender.Draw.Toggle('Y',               12,  x(1)+w(1)/3,  y(5), w(1)/3, h(1), copyResY, 'Copy Y resolution from current (last) block')
    Blender.Draw.Toggle('Z',               13,  x(1)+w(2)/3,  y(5), w(1)/3, h(1), copyResZ, 'Copy Z resolution from current (last) block')
    Blender.Draw.Button('Write to dict.',   2,  x(0),  y(4), w(2), h(1), 'Write all points and registred blocks')
    Blender.Draw.Button('Clear blocks',    10,  x(0),  y(3), w(2), h(1), 'Clear out all selections')
    Blender.Draw.Button('Write and quit',   4,  x(0),  y(1), w(1), h(1), 'Write the complete blockMeshDict. Overwrites!')
    Blender.Draw.Button('Quit, no write',   5,  x(1),  y(1), w(1), h(1), 'Quit')
    resX = Blender.Draw.Number('x-res: ',  8,  x(2),  y(5), w(1), h(1), blockEngine.currentBlock.res[0],1,100,'Block x direction resolution')
    resY = Blender.Draw.Number('y-res: ',  8,  x(3),  y(5), w(1), h(1), blockEngine.currentBlock.res[1],1,100,'Block y direction resolution')
    resZ = Blender.Draw.Number('z-res: ',  8,  x(4),  y(5), w(1), h(1), blockEngine.currentBlock.res[2],1,100,'Block z direction resolution')
    blockIndex = Blender.Draw.Number('Index: ',  9,  x(2),  y(4), w(3), h(1), blockEngine.currentBlockIndex, 0, max(0,len(blockEngine.blocks)-1), 'Select block by its index')
    Blender.Draw.Button('Triangle normal',    25,  x(4),  y(1), w(1), h(1), 'Select 3 verts and get the triangle normal')

def event(evt,val):  
    global exportFileName
    global blockEngine
    global blockIndex
    global resX, resY, resZ
    global copyResX, copyResY, copyResZ

    if not val:
        if evt == Blender.Draw.RIGHTMOUSE:
            blockEngine.collectBlock(unselect=True)
            if copyResX:
                blockEngine.currentBlock.res[0] = resX.val
            if copyResY:
                blockEngine.currentBlock.res[1] = resY.val
            if copyResZ:
                blockEngine.currentBlock.res[2] = resZ.val
            blockEngine.showBlock(False)
        elif evt == Blender.Draw.MIDDLEMOUSE:
            blockEngine.removeBlock()
            blockEngine.showBlock(True)
        else:
            return
    else:
        return
    Blender.Draw.Redraw(1)
 
def getFileName(fileName):
    global exportFileName
    exportFileName = fileName

def button(evt):
    global exportFileName
    global blockEngine
    global blockIndex
    global resX, resY, resZ
    global copyResX, copyResY, copyResZ

    if evt == 1: 
        Blender.Window.FileSelector(getFileName,'Export')
 
    if evt == 2: 
        blockEngine.writeDict(final = True)

    if evt == 4:
        blockEngine.writeDict(final = True)
        Blender.Draw.Exit()

    if evt == 5:
        Blender.Draw.Exit()

    if evt == 6:
        blockEngine.writeDict(pointSelection='selected',writeBlock=False)

    if evt == 7:
        blockEngine.collectBlock()
        if copyResX:
            blockEngine.currentBlock.res[0] = resX.val
        if copyResY:
            blockEngine.currentBlock.res[1] = resY.val
        if copyResZ:
            blockEngine.currentBlock.res[2] = resZ.val
        blockEngine.showBlock(True)

    if evt == 8:
        infoString = ''
        if blockEngine.currentBlockIndex >= 0:
            blockEngine.currentBlock.res = [resX.val, resY.val, resZ.val]
            blockEngine.currentBlock.copyToNeighbours(blockEngine.blocks)
            infoString = 'Current block (%i) res = %i %i %i' % ((blockEngine.currentBlockIndex,) + tuple(blockEngine.currentBlock.res))
        else:
            infoString = 'No block currently registred'
        blockEngine.info(infoString)

    if evt == 9:
        blockEngine.selectByIndex(blockIndex.val)
        if copyResX:
            blockEngine.currentBlock.res[0] = resX.val
        if copyResY:
            blockEngine.currentBlock.res[1] = resY.val
        if copyResZ:
            blockEngine.currentBlock.res[2] = resZ.val
        blockEngine.showBlock(True)
        Blender.Redraw()

    if evt == 10:
        blockEngine.clear()

    if evt == 11:
        copyResX = 1-copyResX
    if evt == 12:
        copyResY = 1-copyResY
    if evt == 13:
        copyResZ = 1-copyResZ

    if evt == 16:
        blockEngine.removeDoubles()

    if evt == 25:
        mm = MeshManipulator()
        normal = mm.facetNormal()
        infoString = ''
        if mm.OK:
            infoString = 'Triangle normal = (%f %f %f)' % (normal.x, normal.y, normal.z)
        else:
            infoString = mm.error
        blockEngine.info(infoString)

    if evt == 35:
        blockEngine.readBlocks()
        Blender.Redraw()
    if evt == 36:
        blockEngine.readPoints()

    Blender.Draw.Redraw(1)

Blender.Draw.Register(gui,event,button)
 
