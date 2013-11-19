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
    parser.add_option('-f','--file',dest='stlFile',default='afile',help='Input stl file')
    parser.add_option('-t','--split',dest='split',action='store_true',default=False,help='Split into separate files')

    options,arguments = parser.parse_args()


    print getattr(options,'stlFile')
    if getattr(options,'stlFile'):
        print 'Missing -f'

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

    return options,arguments


getArgs()
