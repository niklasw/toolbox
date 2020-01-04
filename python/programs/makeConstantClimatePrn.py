#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

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
    parser.add_option('-T','--temperature',dest='temperature',default=None,help='Constant air temp')
    parser.add_option('-H','--Rh',dest='Rh',default=50,help='Constant relative humidity')
    parser.add_option('-W','--wind',dest='wind',default=0.0,help='Wind speed')
    parser.add_option('-o','--output',dest='output',default=None,help='Output file')

    options,arguments = parser.parse_args()

    if options.output is None:
        print 'Missing --output'

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

    options.wind = validateOption(options.wind,float)
    options.temperature = validateOption(options.temperature,float)
    options.Rh = validateOption(options.Rh,float)

    return options,arguments

def mkConstantClimate(T,Rh,W,outFile,nh=8784):
    with open(outFile,'w') as fp:
        for i in range(1,nh+1):
            fp.write('{0:d} {1:f} {2:f} {3:f} 0 0 0\n'.format(i,T,Rh,W))

if __name__=="__main__":
    o,a = getArgs()
    mkConstantClimate(o.temperature,o.Rh,o.wind,o.output)
