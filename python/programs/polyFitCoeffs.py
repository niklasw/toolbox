#!/usr/bin/env python

from pylab import *
import sys,os

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
    from optparse import Values as optValues
    descString = """
    Python thing to find best polynomial coefficients for curve fit.
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--filename',dest='filename',default=None,help='Input data file. Two columns.')
    parser.add_option('-s','--skiprows',dest='skiprows',default='0',help='Number of rows to skip (from file start.)')
    parser.add_option('-d','--delimiter',dest='delimiter',default=' ',help='Column delimiter. e.g. ","')
    parser.add_option('-m','--maxorder',dest='maxorder',default=6,help='Higest polynomial order to evaluate')

    options,arguments = parser.parse_args()

    if  not options.filename:
        Error( 'Missing indata file (-f filename)' )

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

    options.skiprows = validateOption(options.skiprows, int)
    options.maxorder = validateOption(options.maxorder, int)

    if not os.path.isfile(options.filename):
        Error('Cannot read file named %s' % options.filename)

    return options,arguments


def printCoeffs(arr):
    # Return string w line feeds of coeffs in reversed order.
    return '\n\t'.join([str(a) for a in arr[::-1]])

def main():

    options,arguments = getArgs()

    print options

    data = load(options.filename,skiprows=options.skiprows,delimiter=options.delimiter)

    x=data[:,0]
    y=data[:,1]

    def fitPoly(x1,x2,order=2):
        coeffs=polyfit(x1,x2,order)
        t=[pow(x1,a) for a in range(order,-1,-1)]
        return coeffs, dot(coeffs,t)

    orderList = range(1,options.maxorder+1)

    plot(x,y,'-ok')
    grid('on')

    lgd=['data']+['order %i' % a for a in orderList]

    for order in orderList:
        coeffs, p = fitPoly(x,y,order)
        plot(x,p)

        Info('Coeffs for polynomial order %i =\n\t%s\n' % (order,printCoeffs(coeffs)))

    legend(lgd)
    show()

if __name__ == '__main__':
    main()

