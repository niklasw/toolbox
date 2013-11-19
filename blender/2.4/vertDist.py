#!BPY

"""
Name: 'Vertex distance'
Blender: 244
Group: 'Export'
Tooltip: 'Export selected orthogonal hex blender mesh to blockMesh format '
"""
__author__ = "Niklas Wikstrom"
__url__ = ("")
__version__ = "1.0 2010-09-11"

__bpydoc__ = """\
Script to output distance between two selected vertices.
"""

# --------------------------------------------------------------------------
# vertDist.py
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

class Coord(list):
    def __init__(self,coord=[0,0,0]):
        list.__init__(self,coord)
        self.x = float(coord[0])
        self.y = float(coord[1])
        self.z = float(coord[2])
        self.coord = coord
    def __str__(self):
        return '(%f %f %f)' % (self.x,self.y,self.z)

class MeshManipulator:
    """Note that here verts is blender points"""
    global message
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

    def vertexPairDistance(self,selected=1):
        global message
        import math
        dist = -1.0
        verts = self.selectedVerts()
        for v in verts: print v.co*self.ob.matrix
        if len(verts) == 2:
            r = verts[1].co*self.ob.matrix-verts[0].co*self.ob.matrix
            dist = math.sqrt(Blender.Mathutils.DotVecs(r,r))
            message = 'Vertex distance = %s\n' % (str(dist))
            message += '  dX, dY, dZ = %f, %f, %f' % (r.x,r.y,r.z)
            print message
        else:
            message = 'Not two verts selected'
        return dist

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

def getFileName(fileName):
    global exportFileName
    exportFileName = fileName

exportFileName='/tmp/vertDist.dat'
message='Nothing to tell'
message2=''

def gui():
    x0= 10
    x = lambda d: d*96 + x0
    y = lambda d: d*20
    w = lambda d: d*96
    h = lambda d: d*20
    Blender.BGL.glClear(Blender.BGL.GL_COLOR_BUFFER_BIT) 
    Blender.BGL.glRasterPos2d(               x0+x(2),  y(7))

    Blender.Draw.Text(message)
    Blender.Draw.Button(exportFileName,     1,  x(0),  y(9), w(2), h(1), 'File selector opens')
    Blender.Draw.Button('Remove doubles',   2,  x(0),  y(8), w(2), h(1), 'Remove all double vertices')
    Blender.Draw.Button('Measure',          3,  x(0),  y(7), w(2), h(1), 'Get distance between vertices')
    Blender.Draw.Button('Triangle normal',  4,  x(0),  y(6), w(2), h(1), 'Select 3 verts and get the triangle normal')
    Blender.Draw.Text(message2)

def event(evt,val):
    pass

def button(evt):
    global message
    if evt == 1: 
        Blender.Window.FileSelector(getFileName,'Export')
    elif evt == 2:
        message='removing doubles'
        n = MeshManipulator().removeDoubles()
        message = 'Removed %i vertices' % n
    elif evt == 3:
        MeshManipulator().vertexPairDistance()
    elif evt == 4:
        mm = MeshManipulator()
        normal = mm.facetNormal()
        infoString = ''
        if mm.OK:
            message = 'Triangle normal = (%f %f %f)' % (normal.x, normal.y, normal.z)
            print message
        else:
            message = mm.error


    pass


Blender.Draw.Register(gui,event,button)
