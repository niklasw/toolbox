#!/usr/bin/python
"""Demo script that converts a series of legacy VTK files (time-steps) to a PVD file
referencing a series of VTU files.
"""

import os,sys
from paraview import servermanager

def findFiles(seekNames, path):
    import glob
    return glob.glob(os.path.join(path,seekNames))

def getArgs():
    from optparse import OptionParser
    import glob
    descStr = 'Python script that converts a series of '
    descStr+= 'legacy VTK files (time-steps or parts) '
    descStr+= 'to a PVD file referencing a series of VTU files.'
    parser=OptionParser(description=descStr)
    parser.add_option('-f','--files',dest='globs',default='*.vtk',help='Shell glob to match files (*.vtk)')
    parser.add_option('-D','--dirs',dest='partDirs',default=None,help='Dirs with legacy part files (processor?/VTK/pipes)')
    parser.add_option('-o','--out',dest='outfile',default='vtus.pvd',help='Resulting merged file')
    parser.add_option('-n','--name',dest='vtuname',default='VTU',help='Trunk name for vtu files')
    parser.add_option('-P','--parts',dest='mkparts',action='store_true',default='False',help='Not used')
    parser.add_option('-N','--ncpus',dest='ncpus',default='1',help='Try to run threaded convert, NOT IMPLEMENTED!')
    (opt,arg) = parser.parse_args() 

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)

    inputDir = os.getcwd()
    if opt.partDirs:
        partDirs = glob.glob(opt.partDirs)

    vtkPartsDict = {}
    for item in partDirs:
        vtkPartsDict[item] = findFiles(opt.globs, item)

    args = {
            'parts':vtkPartsDict,
            'outfile':opt.outfile,
            'nCpus':int(opt.ncpus)
           }
    return args

def vtk_to_vtu(in_file, out_file):
    "Convert one vtk file to a vtu file"
    reader = servermanager.sources.LegacyVTKFileReader(FileNames=in_file)
    writer = servermanager.writers.XMLUnstructuredGridWriter(Input=reader, FileName=out_file)
    writer.UpdatePipeline()

def sortFilesByIndex(fileList):
    indexedList = {}
    for f in fileList:
        index = int ( os.path.splitext(f)[0].split('_')[-1] )
        if not indexedList.has_key(index):
            indexedList[index] = []
        indexedList[index].append(f)
    return indexedList

def writePvdHead(fptr):
    fptr.write("""<?xml version="1.0"?>
<VTKFile type="Collection" version="0.1" byte_order="LittleEndian" compressor="vtkZLibDataCompressor">
  <Collection>
""")

def writePvdInstance(fptr,index, part, afile):
    fptr.write('    <DataSet timestep="%d" group="" part="%d" file="%s"/>\n' % (index, part, afile))

def writePvdFoot(fptr):
    fptr.write("""  </Collection>
</VTKFile>
""")

class partsContainer:
    class part:
        def __init__(self,partPath,partName,partIndex,filesDict):
            self.name = partName
            self.path = partPath
            self.index = partIndex
            self.files = filesDict
            self.nFiles = len(self.files.keys())

        def convert(self,outDir,pvdFilePtr):
            import string
            for timeIndex in self.files.keys():
                files = self.files[timeIndex]
                outPath = os.path.join(
                      outDir,
                      self.name
                      + '_' + str(self.index)
                      + '_' + string.zfill(timeIndex,4)
                      + '.vtu')
                print "Converting %s at time %d to %s" % (self.path, timeIndex, outPath)
                vtk_to_vtu(files,outPath)
                writePvdInstance(pvdFilePtr,timeIndex,self.index,outPath)
        
    def __init__(self):
        self.parts = []
        self.nparts = 0

    def dirToPartName(self,dirStr):
        import re
        dirStr = re.sub('\/','_',dirStr)
        return   re.sub('VTK','',dirStr)

    def getPartIndex(self,partStr):
        import re
        pat = re.compile('[0-9]+')
        numbers = pat.findall(partStr)
        number = int(0)
        if len(numbers) > 0:
            number = int(numbers[0])
        return number

    def add(self,partPath,fileDict):
        partName = self.dirToPartName(partPath)
        partIndex = self.getPartIndex(partName)
        self.parts.append(self.part(partPath,partName,partIndex,fileDict))
        self.nparts = len(self.parts)

def main():
    import string, thread
    from processing import Process, Queue
    if not servermanager.ActiveConnection:
        connection = servermanager.Connect()

    args = getArgs()

    vtk_partsDict = args['parts']
    out_file = args['outfile']
    nCpus = args['nCpus']
    vtu_dir = os.path.splitext(out_file)[0]+'_vtu'

    parts = partsContainer()
    for partPath,files in vtk_partsDict.iteritems():
        filesDict = sortFilesByIndex(files)
        parts.add(partPath,filesDict)

    try:
        os.mkdir(vtu_dir)
    except:
        pass

    f_out = file(out_file, 'w')
    writePvdHead(f_out)

    if nCpus > 1:
        print "PARALLEL RUN NOT IMPLEMENTED"
        sys.exit(1)
        i = 0
        while i < parts.nparts:
            lock=thread.allocate_lock()
            p = []
            for cpu in range(nCpus):
                part = parts.parts[i]
                print '\n*** Launching process',i
                #thread.start_new_thread(part.convert,(vtu_dir,f_out,))
                p[i] = Process(target=part.convert, args = [vtu_dir, f_out])
                p[i].start()
                i+=1
    else:
        for part in parts.parts:
            part.convert(vtu_dir,f_out)

    writePvdFoot(f_out)

    f_out.close()

if __name__ == "__main__":
    main()
