#!BPY

"""
Name: 'Edge mesh exporter'
Blender: 244
Group: 'Export'
Tooltip: 'Export selected edges as an edge mesh'
"""
import Blender
import bpy

def getSelectedEdges():
    in_editmode = Blender.Window.EditMode()
    if in_editmode: 
        Blender.Window.EditMode(0)
    object = Blender.Object.GetSelected()[0]
    data = object.getData()
    # Get only selected edges
    selEdges = [ e for e in data.edges if e.v1.sel == 1 and e.v2.sel == 1 ]
    print "Got %i selected edges" % len(selEdges)
    if in_editmode: 
        Blender.Window.EditMode(1)
    return selEdges

def writeEdges(filename):
    out = file(filename+'.obj', "w")
    count = 1
    for edge in getSelectedEdges():
        out.write('v %f %f %f\n' % (edge.v1.co.x, edge.v1.co.y, edge.v1.co.z))
        out.write('v %f %f %f\n' % (edge.v2.co.x, edge.v2.co.y, edge.v2.co.z))
        out.write('l %i %i\n' % (count, count+1))
        count += 2

Blender.Window.FileSelector(writeEdges, "Export")

