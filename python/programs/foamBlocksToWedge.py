#!/usr/bin/python


import os,sys,sre,math,fileinput

prog=os.path.basename(sys.argv[0])

def usage(exit=True):
    print "\nUsage:\n",prog," <blockMeshDict file>"
    print """
    This python script needs a blockMeshDict
    file as argument , containing block vertices to be modified.

    Some or several of these criteria is not met.
    """
    if(exit):
        print "Exiting.\n"
        sys.exit(1)

sys.path.append('/home/nikwik/toolbox/python/')
from myRePatterns import *
try:
    blockMeshDict=sys.argv[1]
except:
    usage()

if not os.path.isfile(blockMeshDict):
    usage()

startpat=wordpat('vertices')

endpat=sre.compile(r'\);')

wedgeangle=5.0
alpha=wedgeangle*math.pi/180.0
tanalpha=math.tan(alpha/2.0)

govertex=False
vertices=[]

print '\nFound the following vertices:\n'
for line in fileinput.input(blockMeshDict):
    if startpat.match(line):
        print line.rstrip()+'\n('
        govertex=True
    if endpat.match(line):
        govertex=False
        # if endpat is matched, quit reading
        fileinput.close()
        print '\n)'
        break

    if govertex:
        if vectorpat.match(line):
            (xs,ys,zs)=parenpat.sub('',line).split()
            vertices.append((float(xs),float(ys),float(zs)))
            print '\t'+line.strip()


fileinput.close()

print '\nReplace by the following:\n'
print 'vertices\n('
for i in range(len(vertices)):
    v=vertices[i]
    x,y,z=float(v[0]),float(v[1]),float(v[2])
    if not z==0.0:
        z=y*tanalpha
    else:
        z=-y*tanalpha
    vertices[i]=(x,y,z)
    print '\t(',x,y,z,')'
print ');'

print '\nEnd\n'

