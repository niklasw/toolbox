#!/usr/bin/env python

from numpy import roots, zeros
import sys

def Error(s,sig=1):
    print '\nError %s!\n' % s
    sys.exit(sig)

def Warn(s):
    output = 'Warning %s!' % s
    print '\n'+'='*len(output)
    print output
    print '='*len(output)

def Info(s):
    print '\t%s' % s

def getArgs():
    from optparse import OptionParser
    descString = """
    Calculate last to first length ratio for Star-CCM+ extrusion, given number of steps and total length.
    """

    parser=OptionParser(description=descString)
    parser.add_option('-n','--nsteps',dest='nsteps',default=20,help='Number of extrusion layers.')
    parser.add_option('-d','--start',dest='start',default=0.01,help='First cell thickness.')
    parser.add_option('-L','--length',dest='length',default=1.0,help='Extrusion length.')
    parser.add_option('-B','--basesize',dest='basesize',default=1.0,help='Base size normalisation.')

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

    opt.nsteps = validateOption(opt.nsteps,int)
    opt.length = validateOption(opt.length,float)
    opt.start  = validateOption(opt.start,float)
    opt.basesize  = validateOption(opt.basesize,float)

    return opt,arg

def calcExpansionRoots(firstCell, N, L):
    # Find roots of equation for the expansion ratio, a,
    # which results from a geometric series.
    # Non real roots and unity is discarded.
    Lr = L/firstCell
    # Set up the coefficient vector for the polynom
    c = zeros(N+1)
    c[0], c[-2], c[-1] = 1, -Lr, Lr-1
    # Calculate roots of polynom and extract only relevant ones.
    realRoots = [ a.real for a in roots(c) if a.imag == 0 and abs(a.real-1.0) > 1e-6 ]
    return realRoots

if __name__ == '__main__':
    opt,arg = getArgs()
    realRoots = calcExpansionRoots(opt.start, opt.nsteps, opt.length)

    expansionRatio = 0.0

    if len(realRoots) == 1:
        expansionRatio = realRoots[0]
    elif len(realRoots) == 0:
        Warn('Did not find any real root that is not unity')
    else:
        Warn('Found more than one real non unity root.')
        print realRoots
        Info('Assuming the largest root is the searched.')
        expansionRatio = max(realRoots)

    Warn('Assuming constant rate stretching')
    Info('Number of layers         = %7i' % opt.nsteps)
    Info('Magnitude                = %7.2e' % opt.length)
    Info('Expansion ratio          = %4.2e' % expansionRatio)
    Info('First cell heigth (input)= %4.2e' % (opt.start/opt.basesize))
    Info('Last  cell heigth (input)= %4.2e' % ((opt.start*expansionRatio**opt.nsteps)/opt.basesize))
    Info('Last to first cell ratio = %4.1e' % expansionRatio**opt.nsteps)






