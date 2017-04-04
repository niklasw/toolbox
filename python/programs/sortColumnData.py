#!/usr/bin/python

from numpy import array, loadtxt
import os,sys

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
    parser.add_option('-d','--delimiter',dest='delimiter',default=',',help='Column field delimiter')
    parser.add_option('-s','--skip',dest='skip',default='0',help='Number of rows to skip')
    parser.add_option('-c','--column',dest='column',default='0',help='Column to sort by')

    options,arguments = parser.parse_args()


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

    options.skip = validateOption(options.skip,int)
    options.column = validateOption(options.column,int)

    fileName = arguments[0]
    if not os.path.isfile(arguments[0]):
        argError('"%s" is not a file I can read' % arguments[0])
    return options,arguments


o,a = getArgs()

dataFile = a[0]
sortCol = o.column
nSkip = o.skip

header=''
with open(dataFile) as fp:
    for i in range(nSkip):
        header+=fp.readline()

data=loadtxt(dataFile,delimiter=o.delimiter,skiprows=nSkip)

sortd = data[data[:,sortCol].argsort()]

sys.stdout.write(header)
for row in sortd:
    line = o.delimiter.join(map(str,row))
    print line


