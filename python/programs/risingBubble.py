#!/usr/bin/env python

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
    Python thing
    """

    parser=OptionParser(description=descString)
    parser.add_option('-d','--diameter',dest='diameter',default=1e-3,help='Bubble diameter')
    parser.add_option('-r','--bubbledensity',dest='bubbledensity',default=1.2,help='Bubble density')
    parser.add_option('-R','--liquiddensity',dest='liquiddensity',default=1e3,help='Liquid density')
    parser.add_option('-v','--nu',dest='nu',default=1e-6,help='Liquid kinamatic viscosity')
    #parser.add_option('-t','--split',dest='split',action='store_true',default=False,help='S'

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

    opt.bubbledensity = validateOption(opt.bubbledensity,float)
    opt.liquiddensity = validateOption(opt.liquiddensity,float)
    opt.diameter      = validateOption(opt.diameter,float)
    opt.nu            = validateOption(opt.nu,float)

    return opt,arg

if __name__=='__main__':
    opt,arg = getArgs()
    D = opt.diameter
    rho_b = opt.bubbledensity
    rho_l = opt.liquiddensity
    nu = opt.nu

    deltaRho = opt.bubbledensity/opt.liquiddensity
    g = 9.81
    #
    # Buoyancy force
    # F_b = (rho_b-rho_l)*g*(4*pi*R**3)/3
    #
    # Stokes law
    #
    # F_d = 6*pi*nu*rho*R*U_term
    #
    #
    U_term=(rho_l-rho_b)/rho_l*g*D**2/18./nu

    Info('Terminal velocity = %.3e' % U_term)






