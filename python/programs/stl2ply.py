#!/usr/bin/env python
import os, struct, sys, string
import time

######################################################

def Error(self,s,sig=1):
    print '\nError %s!\n' % s
    sys.exit(sig)

def Warn(self,s):
    output = 'Warning %s!' % s
    print '\n'+'='*len(output)
    print output
    print '='*len(output)

def Info(self,s):
    print '\t%s' % s

def getArgs():
    from optparse import OptionParser
    descString = """
    Python thing to scale stl file vertices
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--file',dest='stlFile',default=None,help='Input stl file')
    parser.add_option('-s','--scale',dest='scale',default=1.0,help='Scale geometry during conversion')

    (opt,arg)=parser.parse_args()

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)

    def validateOption(option, test, msg='Invalid argument', allowed=[]):
        try:    option = test(option)
        except: argError('%s; got %s' % (msg,option))
        if allowed and not option in allowed:
            argError('%s; got %s. Allowed values are %s' % (msg,option,allowed))
        return option

    opt.scale = validateOption(opt.scale,float)

    if not os.path.isfile(opt.stlFile):
        argError('Stl file not found: %s' % opt.stlFile)

    return opt,arg

def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper

@print_timing
def read_file(filename,scale):
    faces = []
    verts = list()

    scaledFloat = lambda s: scale*float(s)
    if scale == 1:
        scaledFloat = lambda s: float(s)

    file = open(filename, "r")

    while True:
        try:
            line = file.next().strip()
            if line[0] == 'v':
                v = map(scaledFloat,line.split()[-3:])
                verts.append(v)
        except:
            print "Finished read file", filename
            break
    file.close()

    faces = range(len(verts))
    faces = [faces[i:i+3] for i in range(0,len(faces),3)]
    return verts,faces

def plyHeader(nverts, nfaces):
    s = ['ply']
    s+= ['format ascii 1.0','comment ...']
    s+= ['element vertex %i'%nverts, 'property float x','property float y','property float z']
    s+= ['element face %i'%nfaces, 'property list uchar int vertex_indices','end_header','']
    return string.join(s,'\n')

@print_timing
def writePly(plyFile, verts, faces):
    head  = plyHeader(len(verts),len(faces))

    fh = open(plyFile,'w')
    fh.write(head)

    for v in verts:
        fh.write('%0.6f %0.6f %0.6f\n' % tuple([a for a in v]))

    for f in faces:
        fh.write('%i '% len(f))
        fh.write(len(f)*' %i'% tuple([a for a in f]))
        fh.write('\n')
    fh.close()

@print_timing
def run():
    opt,arg = getArgs()
    plyFile = os.path.splitext(opt.stlFile)[0]+'.ply'
    verts,faces = read_file(opt.stlFile,opt.scale)
    writePly(plyFile,verts,faces)


if __name__=='__main__':
    run()

