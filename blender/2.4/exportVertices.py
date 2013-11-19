#!BPY

"""
Name: 'Vertex blockMesh Exporter'
Blender: 244
Group: 'Export'
Tooltip: 'Export vertices of a mesh object'
"""
import Blender
import bpy
import operator
import sys

def sortTable(table, order=(0), reverse=False):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list 
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    if order.__class__ == tuple:
        for col in reversed(order):
            table = sorted(table, key=operator.itemgetter(col),reverse=reverse)
    else:
        col = order
        table = sorted(table, key=operator.itemgetter(col),reverse=reverse)
    return table

def getSelectedPoints():
    """ a point is here a tuple of (i, x, y, z)"""
    in_editmode = Blender.Window.EditMode()
    if in_editmode: 
        Blender.Window.EditMode(0)
    object = Blender.Object.GetSelected()[0]
    data = object.getData()
    data.transform(object.matrixWorld)
    # Get only selected verts
    # Call them points, to separate from blender vert
    points = [ (v.index, v.co.x, v.co.y, v.co.z) for v in data.verts if v.sel == 1 ]
    if in_editmode: 
        Blender.Window.EditMode(1)
    return points

def writePoints(filename):
    out = file(filename+'.vrt', "w")
    points = getSelectedPoints()
    #points = sortPoints(points)
    for v in points:
        # Due to tolerance questions, only print 3 decs.
        out.write('\t%6i (%8.3f %8.3f %8.3f)\n' % v)

Blender.Window.FileSelector(writePoints, "Export")

