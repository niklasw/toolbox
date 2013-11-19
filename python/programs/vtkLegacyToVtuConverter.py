"""Demo script that converts a legacy VTK file to a VTU file.
"""

from paraview import servermanager

INPUTFILE = ["/home/nikwik/VTK/andritz_2800.vtk","VTK/primairnose/primairnose_2800.vtk"]
OUTPUTFILE = "andritz_2800.vtu"

# create a built-in connection
if not servermanager.ActiveConnection:
    connection = servermanager.Connect()

# create reader for legacy VTK files
reader = servermanager.sources.LegacyVTKFileReader(FileNames=INPUTFILE)

# create VTU writer and connect it to the reader
writer = servermanager.writers.XMLUnstructuredGridWriter(Input=reader,
                                                         FileName=OUTPUTFILE)

# Trigger execution of pipeline
writer.UpdatePipeline()
