#!BPY

""" Registration info for Blender menus:
Name: 'Named ascii STL file (.stl)...'
Blender: 243
Group: 'Export'
Tip: 'Export selected meshes to ASCII STL (.stl) format'
"""

__author__ = "Andrew King"
__url__ = ("")
__version__ = "0.1 2008-07-28"

__bpydoc__ = """\
This script exports selected Blender meshes to an ASCII STL, with object names.
"""

# --------------------------------------------------------------------------
# ASCIISTLExport version 0.1
# Program versions: Blender 2.42+ 
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2008: Andrew King
# Based on AC3DExport (Willian Germano), and blendobjs2stl.0.1.py (Giorgio Griffon)
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
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# --------------------------------------------------------------------------

import Blender
from Blender import NMesh, Object, Mesh, Material, Image, Registry
from Blender import sys as bsys

# Globals
REPORT_DATA = {
	'main': [],
	'errors': [],
	'warns': []
}

# flags:
LOOSE = Mesh.EdgeFlags['LOOSE']
FACE_TWOSIDED = Mesh.FaceModes['TWOSIDE']
MESH_TWOSIDED = Mesh.Modes['TWOSIDED']

REG_KEY = 'asciistl_export'

# config options:
GLOBAL_COORDS = True
ONLY_SELECTED = True
EXPORT_DIR = ''

tooltips = {
	'GLOBAL_COORDS': "transform all vertices of all meshes to global coordinates",
	'ONLY_SELECTED': "export only selected objects",
}

def update_RegistryInfo():
	d = {}
	d['EXPORT_DIR'] = EXPORT_DIR
	d['ONLY_SELECTED'] = ONLY_SELECTED
	d['tooltips'] = tooltips
	d['GLOBAL_COORDS'] = GLOBAL_COORDS
	Registry.SetKey(REG_KEY, d, True)

# Looking for a saved key in Blender.Registry dict:
rd = Registry.GetKey(REG_KEY, True)

if rd:
	try:
		EXPORT_DIR = rd['EXPORT_DIR']
		GLOBAL_COORDS = rd['GLOBAL_COORDS']
	except KeyError: update_RegistryInfo()

else:
	update_RegistryInfo()

VERBOSE = True
CONFIRM_OVERWRITE = True

# check General scripts config key for default behaviors
rd = Registry.GetKey('General', True)
if rd:
	try:
		VERBOSE = rd['verbose']
		CONFIRM_OVERWRITE = rd['confirm_overwrite']
	except: pass

class ASCIISTLExport: # the ac3d exporter part

	def __init__(self, scene_objects, file):

		self.file = file
		objs = [o for o in scene_objects if o.type == 'Mesh']


		# not sure if needed
		# create a temporary mesh to hold actual (modified) mesh data
		TMP_mesh = Mesh.New('tmp_for_stl_export')

		# write the objects

		for obj in objs:
			self.obj = obj

			objtype = obj.type
			objname = obj.name

			mesh = TMP_mesh # temporary mesh to hold actual (modified) mesh data
			mesh.getFromObject(objname)
			self.mesh = mesh
			self.export_mesh(mesh, obj)

	def export_mesh(self, mesh, obj):
		file = self.file
		name=obj.name
		meshname = obj.getData(name_only = True)
		nmesh=NMesh.GetRaw(meshname)
		nmesh.transform(obj.matrixWorld)
		file.write("solid "+name+"\n")
		
		n_tri=0 # number of tris in STL
		n_face=len(nmesh.faces)
		for i in range(0,n_face):
			face=nmesh.faces[i]
			nx=face.no[0]
			ny=face.no[1]
			nz=face.no[2]
			n_vert=len(face.v)
			if n_vert>2:
				file.write("facet normal "+str(nx)+" "+str(ny)+" "+str(nz)+"\n")
				file.write("  outer loop")
				for j in range(0,3):
					vert=face.v[j]
					file.write("\n    vertex")
					for k in range(0,3):
						file.write(" "+str(vert[k]))
				file.write("\n  endloop\n")
				file.write("endfacet\n")
				n_tri=n_tri+1
				if n_vert>3:
					file.write("facet normal "+str(nx)+" "+str(ny)+" "+str(nz)+"\n")
					file.write("  outer loop")
					for j in [0,2,3]:
						vert=face.v[j]
						file.write("\n    vertex")
						for k in range(0,3):
							file.write(" "+str(vert[k]))
					file.write("\n  endloop\n")
					file.write("endfacet\n")
					n_tri=n_tri+1
		file.write("endsolid\n")


# End of Class ASCIISTLExport

from Blender.Window import FileSelector

def report_data():
	global VERBOSE

	if not VERBOSE: return

	d = REPORT_DATA
	msgs = {
		'0main': '%s\nExporting meshes to ASCII STL format' % str(19*'-'),
		'1warns': 'Warnings',
		'2errors': 'Errors',
	}
	keys = msgs.keys()
	keys.sort()
	for k in keys:
		msgk = msgs[k]
		msg = '\n'.join(d[k[1:]])
		if msg:
			print '\n-%s:' % msgk
			print msg

# File Selector callback:
def fs_callback(filename):
	global EXPORT_DIR, OBJS, CONFIRM_OVERWRITE, VERBOSE

	if not filename.endswith('.stl'): filename = '%s.stl' % filename

	if bsys.exists(filename) and CONFIRM_OVERWRITE:
		if Blender.Draw.PupMenu('File Exists!%t|Overwrite') != 1:
			return

	Blender.Window.WaitCursor(1)
	starttime = bsys.time()

	export_dir = bsys.dirname(filename)
	if export_dir != EXPORT_DIR:
		EXPORT_DIR = export_dir
		update_RegistryInfo()

	try:
		file = open(filename, 'w')
	except IOError, (errno, strerror):
		error = "IOError #%s: %s" % (errno, strerror)
		REPORT_DATA['errors'].append("Saving failed - %s." % error)
		error_msg = "Couldn't save file!%%t|%s" % error
		Blender.Draw.PupMenu(error_msg)
		return

	try:
		test = ASCIISTLExport(OBJS, file)
	except:
		file.close()
		raise
	else:
		file.close()
		endtime = bsys.time() - starttime
		REPORT_DATA['main'].append("Done. Saved to: %s" % filename)
		REPORT_DATA['main'].append("Data exported in %.3f seconds." % endtime)

	if VERBOSE: report_data()
	Blender.Window.WaitCursor(0)


# -- End of definitions

scn = Blender.Scene.GetCurrent()

if ONLY_SELECTED:
	OBJS = list(scn.objects.context)
else:
	OBJS = list(scn.objects)

if not OBJS:
	Blender.Draw.PupMenu('ERROR: no objects selected')
else:
	fname = bsys.makename(ext=".stl")
	if EXPORT_DIR:
		fname = bsys.join(EXPORT_DIR, bsys.basename(fname))
	FileSelector(fs_callback, "Export ASCII STL", fname)
