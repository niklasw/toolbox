#!/usr/bin/python

import vtk, os, sys

class GridActors:
    def __init__(self, dataFile):
        self.dataFile=dataFile
        self.reader=vtk.vtkUnstructuredGridReader()
        self.reader.SetFileName(dataFile)
        self.faceFilter=vtk.vtkGeometryFilter()
        self.faceFilter.SetInput(self.reader.GetOutput())
        self.faceActor=vtk.vtkActor()
        self.edgeFilter=vtk.vtkExtractEdges()
        self.edgeFilter.SetInput(self.faceFilter.GetOutput())
        self.edgeActor=vtk.vtkActor()

    def setActor(self,actor,filter):
        mapper=vtk.vtkPolyDataMapper()
        mapper.SetInput(filter.GetOutput())
        mapper.ScalarVisibilityOff()
        actor.SetMapper(mapper)

class MyWindow:
    def __init__(self):
        self.win=vtk.vtkRenderWindow()
        self.ren=vtk.vtkRenderer()
        self.ren.SetBackground(0,0,0)
        self.ren.GetActiveCamera().SetParallelProjection(1)
        self.cam=self.ren.GetActiveCamera()
        self.win=vtk.vtkRenderWindow()
        self.win.SetSize(700,400)
        self.win.AddRenderer(self.ren)
        self.G=''

    def readFile(self,fileName):
        self.G=GridActors(fileName)

    def edges(self):
        G=self.G
        G.setActor(G.edgeActor,G.edgeFilter)
        G.edgeActor.GetProperty().SetColor(0.8,0.6,0.4)
        self.ren.AddActor(G.edgeActor)
        self.win.Render()

    def faces(self):
        G=self.G
        G.setActor(G.faceActor,G.faceFilter)
        self.ren.AddActor(G.faceActor)
        self.win.Render()

    def clear(self):
        self.ren.RemoveActor(self.G.edgeActor)
        self.ren.RemoveActor(self.G.faceActor)
        self.win.Render()

    def render(self):
        self.win.Render()

    def zoom(self,factor):
        self.ren.GetActiveCamera().Zoom(factor)
        self.win.Render()

    def bg(self,r,b,g):
        self.ren.SetBackground(r,b,g)
        self.win.Render()

    def size(self,x,y):
        self.win.SetSize(x,y)
        self.win.Render()

    iren=vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()

render(sys.argv[1])

