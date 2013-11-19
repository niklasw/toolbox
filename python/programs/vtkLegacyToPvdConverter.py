"""Demo script that converts a series of legacy VTK files (time-steps) to a PVD file
referencing a series of VTU files.
"""

import os
from paraview import servermanager

OUTPUTFILE = "/scratch/geus/emtbos.250.pvd"

def get_input_file_list(time_steps):
    "Create list of vtk files to be converted"
    input_dir = "/scratch0/shared/oswald/cedp/emtbos.250/numsol_0"
    file_list = []
    for step in time_steps:
        vtk_file = os.path.join(input_dir, "pitdi250tsno%d.vtk" % int(step))
        file_list.append(vtk_file)
    return file_list

def vtk_to_vtu(in_file, out_file):
    "Convert one vtk file to a vtu file"
    reader = servermanager.sources.LegacyVTKFileReader(FileNames=in_file)
    writer = servermanager.writers.XMLUnstructuredGridWriter(Input=reader,
                                                             FileName=out_file)
    writer.UpdatePipeline()

def main():
    "main program"
    # create a built in connection
    if not servermanager.ActiveConnection:
        connection = servermanager.Connect()

    # get list of vtk files
    time_steps = range(0, 5000)
    vtk_files = get_input_file_list(time_steps)

    # convert to vtu and create pvd file
    out_dir = OUTPUTFILE + ".d"
    try:
        os.mkdir(out_dir)
    except:
        pass
    f_out = file(OUTPUTFILE, "w")
    f_out.write("""<?xml version="1.0"?>
<VTKFile type="Collection" version="0.1" byte_order="LittleEndian" compressor="vtkZLibDataCompressor">
  <Collection>
""")
    for i, in_path in enumerate(vtk_files):
        in_dir, in_file = os.path.split(in_path)
        out_path = os.path.join(out_dir, os.path.splitext(in_file)[0] + ".vtu")
        print "Converting %s to %s" % (in_path, out_path)
        vtk_to_vtu(in_path, out_path)
        f_out.write('    <DataSet timestep="%d" group="" part="0" file="%s"/>\n' % (i, out_path))
    f_out.write("""  </Collection>
</VTKFile>
""")
    f_out.close()

if __name__ == "__main__":
    main()
