import bpy
import bmesh
import os

# Get the active object
obj = bpy.context.active_object

# Ensure the object is in edit mode
if obj.mode != 'EDIT':
    bpy.ops.object.mode_set(mode='EDIT')

# Get the bmesh representation of the object
bm = bmesh.from_edit_mesh(obj.data)

# Get the selected vertices
selected_verts = {v for v in bm.verts if v.select}
selected_verts_i = {v.index for v in selected_verts}

# Get the edges between the selected vertices
selected_edges = []
for edge in bm.edges:
    v1, v2 = edge.verts
    if v1.index in selected_verts_i and v2.index in selected_verts_i:
        selected_edges.append((v1.index, v2.index))

# Print the selected edges
print("Selected edges:", selected_edges)


def write_vertices_header(verts, fp):
    n = len(verts)
    fp.write(f'{n} 2 1 0{os.linesep}')


def write_vertices(verts, fp, offset=1):
    write_vertices_header(verts, fp)
    for i, v in enumerate(verts):
        fp.write(f'{i+offset} {v.co.x} {v.co.y}{os.linesep}')


def write_edges_header(edges, fp):
    n = len(edges)
    fp.write(f'{n} 0 {os.linesep}')


def write_edges(edges, fp, offset=1):
    write_edges_header(edges, fp)
    for i, e in enumerate(edges):
        fp.write(f'{i+offset} {e[0] + offset} {e[1] + offset}{os.linesep}')


def write_holes(holes, fp, offset=1):
    fp.write(f'{len(holes)}{os.linesep}')
    for i, h in enumerate(holes):
        fp.write(f'{i+offset} {h[0]} {h[1]}{os.linesep}')


with open('/tmp/test.poly','w') as f:
    write_vertices(selected_verts, f)
    write_edges(selected_edges, f)
    write_holes([(0, 0)], f)

# Optionally, you can switch back to object mode
bpy.ops.object.mode_set(mode='OBJECT')
