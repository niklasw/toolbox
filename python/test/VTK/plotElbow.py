import os,sys
from vtk import * 
#Check if your linux distribution has this library. 
#In Debian it is called python-vtk.

#set the fileName for the current case (VTK Legacy format)
#Use foamToVTK on the elbow case first!
myFileName = sys.argv[1]

#Need a reader suited to OpenFOAM unstructured grid
reader = vtkUnstructuredGridReader()
reader.SetFileName(myFileName)
reader.Update()

#In OpenFOAM all results are stored as Field-data. 
#This has no concept of cells or nodes. Need to Filter to cells.
toCellFilter = vtkFieldDataToAttributeDataFilter()
toCellFilter.SetInput(reader.GetOutput())
toCellFilter.SetInputFieldToCellDataField()
toCellFilter.SetOutputAttributeDataToCellData()
#Each filter can hold one scalar and one vector data. 
#Assign here which field we are interested in.
#Below syntax is "To the first scalar component (0) 
#assign the first component (0) of the p-field" 
toCellFilter.SetScalarComponent(0,'p',0)

#This is all we need to do do calculations with the data. 
#To get 3D image, need some more components. 

#First a rendering window
renWin = vtkRenderWindow()
#we can set a size here
renWin.SetSize(1024,800)

#Then a renderer. This takes care of rendering 
#our data to an image.
ren1 = vtkRenderer()

#Add renderer to window
renWin.AddRenderer(ren1)

#Now we need to add our pressure data to the renderer. This is done
#by a mapper. Mapping assigns data to colors and a geometry.
mapper = vtkDataSetMapper()
mapper.SetInput(toCellFilter.GetOutput())

#The object is assigned to an actor. This actor 
#can be rotated, scaled etc. 
actor = vtkActor()
actor.SetMapper(mapper)

#Add actor to renderer.
ren1.AddActor(actor)

#Save output as an image
w2if = vtkWindowToImageFilter()
w2if.SetInput(renWin)
#Finally render image
renWin.Render()

wr =vtkPNGWriter()
wr.SetInputConnection(w2if.GetOutputPort())
wr.SetFileName("elbow_pressure.png")
wr.Write()


#Instead of just rendering. We could add some 
#code so that we can interact with 
#the data using a mouse. In this case,
#uncomment the renWin.Render() command above!
#!Uncomment this to get interaction!#
#iren = vtkRenderWindowInteractor()
#iren.SetRenderWindow(renWin)
#iren.Initialize()
#iren.Start()

