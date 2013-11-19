#!/usr/bin/env python

import sys
from stlTool import stlToolBox


class BoundingBlockMesh:

    def __init__(self,fileName,scale = 1.0):
        self.fileName = fileName
        self.rez = [1,1,1]
        self.block = range(8)
        self.longRez = 80
        self.scale = scale

        self.createBlock()

    def __str__(self):
        s = self.printHead(scale = self.scale)
        s += self.printVerts()
        s += self.printBlock()
        s += self.printEdges()
        s += self.printBoundary()
        s += self.printMerge()
        return s

    def write(self,out='blockMeshDict'):
        fp = file(out,'w')
        fp.write(self.__str__())
        fp.close()

    def createBlock(self, name=''):
        from pylab import array,zeros,where,asarray

        tool = stlToolBox(self.fileName,'',False)

        min,max = tool.calcBounds(name)
        max = asarray(max)
        min = asarray(min)
        # Extend the bounding box by 5% (ad hoc) in each direction
        max += abs(max)*0.05
        min -= abs(min)*0.05
        diagonal = max - min
        longestEdge = diagonal.max()

        block = self.block
        block[0] = (min[0],min[1],min[2])
        block[1] = (max[0],min[1],min[2])
        block[2] = (max[0],max[1],min[2])
        block[3] = (min[0],max[1],min[2])

        block[4] = (min[0],min[1],max[2])
        block[5] = (max[0],min[1],max[2])
        block[6] = (max[0],max[1],max[2])
        block[7] = (min[0],max[1],max[2])

        self.rez = map(int,diagonal*self.longRez/longestEdge)

    def printHead(self, scale=1.0):
        head="""/*--------------------------------*- C++ -*----------------------------------*\\
|=========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  2.0.0                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

"""
        head += 'convertToMeters %f;\n' % scale;
        return head

    def printVerts(self):
        verts='\nvertices\n(\n'
        for v in self.block:
            verts += '\t( %f %f %f )\n' % (v[0],v[1],v[2])
        verts += ');\n'
        return verts

    def printBlock(self):
        r = self.rez
        blocks = '\nblocks\n('
        blocks += '\n\thex (0 1 2 3 4 5 6 7) (%i %i %i) simpleGrading (1 1 1)'% (r[0],r[1],r[2])
        blocks += '\n);\n'
        return blocks

    def printEdges(self):
        boundary = '\nedges\n('
        boundary += '\n);\n'
        return boundary

    def printBoundary(self):
        boundary = '\nboundary\n('
        boundary += '\n);\n'
        return boundary

    def printMerge(self):
        boundary = '\nmergePatchPairs\n('
        boundary += '\n);\n'
        return boundary

if __name__=='__main__':
    stlFile = sys.argv[1]

    B = BoundingBlockMesh(stlFile,scale=1.0)
    B.createBlock()
    print B
    B.write()
