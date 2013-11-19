#!/usr/bin/env python

import vtk,sys,os

datafile = sys.argv[1];

reader = vtk.vtkUnstructuredGridReader()

reader.SetFileName(datafile)

reader.Update()

toCellFilter = vtkFieldDataToAttributeDataFilter()

reader.SetScalarsName("p")

toCellFilter = vtkFieldDataToAttributeDataFilter()
toCellFilter = vtkFieldDataToAttributeDataFilter()
toCellFilter = vtkFieldDataToAttributeDataFilter()

cdata = vtk.vtkCellData()

cdata.SetInput(reader.GetOutput())


