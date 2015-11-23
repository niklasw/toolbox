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

def toDeg(r):
   return r*180.0/pi

def toRad(d):
   return d*pi/180

class rotationMatrix:
    '''Input rotation in degrees!'''

    def __init__(self,phiX,phiY,phiZ):
        self.phiX=toRad(phiX)
        self.phiY=toRad(phiY)
        self.phiZ=toRad(phiZ)

    def __str__(self):
        return str((self.phiX,self.phiY,self.phiZ))

    def X(self):
       p=self.phiX
       return matrix([[1, 0,        0       ], \
                      [0, cos(p),   -sin(p)  ], \
                      [0, sin(p),  cos(p)  ]])
    def Y(self):
       p=self.phiY
       return matrix([[cos(p),  0, -sin(p) ], \
                      [0,       1, 0      ], \
                      [sin(p), 0, cos(p) ]])
    def Z(self):
       p=self.phiZ
       return matrix([[cos(p),  -sin(p),  0 ], \
                      [sin(p), cos(p),  0 ], \
                      [0,       0,       1 ]])

    def rotate(self,V,order='xyz'):
        funDict={'x':self.X, 'y':self.Y, 'z':self.Z}
        A = matrix(V).transpose()
        for xyz in order:
            A = funDict[xyz]()*A
        return array(A.transpose())[0]


def getArgs():
    from optparse import OptionParser
    from optparse import Values as optValues
    descString = """
    Python thing to rotate a vector in space. Degrees.
    """

    parser=OptionParser(description=descString)
    parser.add_option('-r','--xyzRotation',dest='xyzRotation',default="(0,0,0)",help='Definition of rotation, X, Y, Z. In that order! "(x y z)"')
    parser.add_option('-v','--originalVector',dest='originalVector',default="(1,0,0)",help='Input vector, to be rotated. "(x y z)"')

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
        rotation = readVector(options.xyzRotation)
        inputVector = readVector(options.originalVector)
    except:
        argError('Could not read options to vectors')

    return (rotation,inputVector)
    #return options.xyzRotation, options.originalVector


rotation, originalVector = getArgs()

M = RM(rotation[0], rotation[1], rotation[2])

vr = M.rotate(originalVector)

print 'rotation =       ({0[0]} {0[1]} {0[2]})'.format(rotation)
print 'input vector =   ({0[0]} {0[1]} {0[2]})'.format(originalVector)
print 'rotated vector = ({0[0]} {0[1]} {0[2]})'.format(vr)
