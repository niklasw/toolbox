#!/usr/bin/env python

import sys,os,re
from subprocess import Popen,PIPE

from interactor import *

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

def getSuites():
    cmd = ['lmutil','lmstat','-a']
    P = Popen(cmd,stdout=PIPE,stderr=PIPE)
    out,err = P.communicate()
    pat = re.compile('^Users of (.*):.*$')
    suites = []
    for line in out.splitlines():
        match = pat.match(line)
        if match:
            suites.append(match.group(1))
    return suites

def getArgs():
    from optparse import OptionParser
    descString = """
    Python thing to check license status
    """

    parser=OptionParser(description=descString)
    parser.add_option('-l','--license',dest='license',default=[],help='Licenses to check. Comma separated')

    (opt,arg)=parser.parse_args()

    def argError(s):
        s = '* ERROR: %s. *' % s
        parser.print_help()
        Error(s)


    def validateOption(option, test, msg='Invalid argument', allowed=[]):
        try:    option = test(option)
        except: argError('%s; got %s' % (msg,option))
        if allowed and not option in allowed:
            argError('%s; got %s. Allowed values are %s' % (msg,option,allowed))
        return option

    validateOption(arg[0],str,allowed=['star'])

    if not opt.license:
        if arg[0] == 'star':
            opt.license=['ccmpsuite','ccmpower']
    else:
        opt.license = opt.license.split(',')

    suites = getSuites()

    for item in opt.license:
        validateOption(item,str,allowed=suites)

    return opt,arg

if __name__=='__main__':
    opt,arg  = getArgs()
    pass

