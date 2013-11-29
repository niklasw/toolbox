#!/usr/bin/python

import sys
from vectorRotation import rotationMatrix as RM

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
    from optparse import Values as optValues
    descString = """
    Python thing to scale stl file vertices
    """

    parser=OptionParser(description=descString)
    parser.add_option('-r','--xyzRotation',dest='xyzRotation',default=(0,0,0),help='Definition of rotation, X, Y, Z. In that order!')
    parser.add_option('-v','--originalVector',dest='originalVector',default=(1,0,0),help='Input vector, to be rotated')

    options,arguments = parser.parse_args()

    def readVector(stringVector):
        vs = stringVector.strip(' ()')
        return map(float, vs.split())

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)

    try:
        print options.xyzRotation
        print options.originalVector
        #rotation = readVector(options.xyzRotation)
        #inputVector = readVector(options.originalVector)
    except:
        argError('Could not read options to vectors')

    #return (rotation,inputVector)
    return options.xyzRotation, options.originalVector


rotation, originalVector = getArgs()

M = RM(rotation, rotation[1], rotation[2])

vr = M.rotate(originalVector)

print 'rotation =       ', rotation
print 'input vector =   ', originalVector
print 'rotated vector = ', vr
