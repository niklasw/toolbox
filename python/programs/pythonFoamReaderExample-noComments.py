#!/usr/bin/python

import os,sys
case=sys.argv[1]
cavityPath = os.path.join(case,'system/controlDict')

from paraview import servermanager

connection = servermanager.Connect()

reader = servermanager.sources.OpenFOAMReader(FileName = cavityPath)
reader.UpdatePipelineInformation()

view = servermanager.GetRenderView()
view = servermanager.CreateRenderView()

rep = servermanager.CreateRepresentation(reader, view)

tsteps = reader.TimestepValues
annTime = servermanager.filters.TimeToTextConvertor(Input=reader)
timeRep = servermanager.rendering.TextSourceRepresentation(Input=annTime)
view.Representations.append(timeRep)
view.ViewTime = max(tsteps)

rep.Representation = 2

lt = servermanager.rendering.PVLookupTable()
rep.LookupTable = lt
rep.ColorAttributeType = 0
rep.ColorArrayName = 'CellToPoint[ptot]'
lt.RGBPoints = [-500, 0, 0, 1, 500, 1, 0, 0]
lt.ColorSpace = 1 # HSV

view.ResetCamera()
cam = view.GetActiveCamera()

view.StillRender()
import time
time.sleep(5)

cam.Elevation(45)

view.StillRender()
time.sleep(5)
