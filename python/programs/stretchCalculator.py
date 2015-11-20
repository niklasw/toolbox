#!/usr/bin/env python

from numpy import roots, zeros, log
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
    parser.add_option('-f','--first',dest='first',default=0.01,help='First cell thickness.')
    parser.add_option('-l','--last',dest='last',default=0.01,help='Last cell thickness.')
    parser.add_option('-L','--length',dest='length',default=1.0,help='Block heigth.')
    parser.add_option('-s','--shortOutput',dest='shortOutput',action='store_true',default=False,help='Only report N')

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

    opt.length = validateOption(opt.length,float)
    opt.first  = validateOption(opt.first,float)
    opt.last  = validateOption(opt.last,float)

    return opt,arg

if __name__ == '__main__':
    opt,arg = getArgs()

    d0 = opt.first
    dn = opt.last
    L  = opt.length
    beta = dn/d0

    eps = 0.0

    N = L*2/(d0+dn) # Guess
    N0 = 10*N
    count = 0
    while abs(N0-N) > 1e-4:
        N0 = N
        eps = pow(beta,(1.0/(N-1))) 
        N  = log(1-L/d0*(1-eps))/log(eps)
        count += 1
    
    if opt.shortOutput:
        sys.stdout.write('{0:0.0f}'.format(round(N)))
    else:
        Info('Convergence in {0} iterations'.format(count))
        Warn('Assuming constant rate stretching')
        Info('Number of layers required= %7.0f' % round(N))
        Info('Total length      (input)= %7.2e' % opt.length)
        Info('Expansion ratio          = %4.2e' % eps)
        Info('First/last ratio         = %4.2e' % (dn/d0) )
        Info('First cell heigth (input)= %4.2e' % opt.first)
        Info('Last  cell heigth (input)= %4.2e' % opt.last)

