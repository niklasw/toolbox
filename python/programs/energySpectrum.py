#!/usr/bin/python

import os,sys,re
from fileParsing import loadArray
import string
try:
    import pylab,numpy
except:
    print 'Python modules pylab and numpy must be installed to run this script'
    sys.exit(1)


prog=os.path.basename(sys.argv[0])

def Info(s,i='Info'):
    s = '! %s: %s' % (i,s)
    n=len(s)
    #print '\t%s\n\t%s\n\t%s' % (n*'-',s,n*'-')
    print '\n\t%s' % (s)

def Error(s):
    Info(s,'Error')
    sys.exit(1)


def getArgs():
    from optparse import OptionParser
    descString = """
    Python thing relying on pylab and numpy to plot 
    energy spectrum from sampled data.
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--file',dest='dataFile',default=None,help='Input file')
    parser.add_option('-i','--image',dest='image',default=None,help='Plot image file')
    parser.add_option('-F','--frq',dest='frq',default=None,help='Sampling frequency')
    parser.add_option('-T','--deltaT',dest='deltaT',default=None,help='Sampling delta T')
    parser.add_option('-c','--column',dest='col',default='0',help='Start column in file to use')
    parser.add_option('-n','--ncol',dest='ncol',default=1,help='Number of columns from start column')
    parser.add_option('-W','--filterWidth',dest='fwidth',default=1,help='Median filtering width')
    parser.add_option('-R','--plotref',dest='plotref',action='store_true',default=False,help='Plot reference -5/3 line')
    parser.add_option('-P','--refpower',dest='refpower',default=1e5,help='Reference line times this value')
    parser.add_option('-l','--log',dest='log',action='store_true',default=False,help='loglog plot')
    parser.add_option('-s','--semilog',dest='semilog',action='store_true',default=False,help='loglog plot')

    (opt,arg)=parser.parse_args()

    def argError(s):
        parser.print_help()
        Error(s)

    if not opt.dataFile: argError( 'Missing file argument' )

    if not opt.frq and not opt.deltaT: argError( 'Missing sample rate information.')

    if not opt.frq: opt.frq = 1.0/float(opt.deltaT)

    fwidth = int(opt.fwidth)
    # Make filter width odd, to work with medfilt
    if numpy.mod(fwidth,2) == 0:
        fwidth += 1

    args={'file':opt.dataFile, \
          'image':opt.image, \
          'f':float(opt.frq), \
          'col':map(int,string.split(opt.col,':')), \
          'ncol':int(opt.ncol),
          'fwidth':fwidth, \
          'plotref':opt.plotref,
          'log':opt.log,
          'refpower':float(opt.refpower),
          'semilog':opt.semilog}

    print 60*'-'
    for key in args.keys():
        print 'Arg:  %-10s= %-15s' % (str(key),str(args[key]))
    print 60*'-'
    return args

def cleanData(stringList):
    dropPat = re.compile('^\s*(?![\(\)\#\/a-zA-Z])')
    parenPat = re.compile('[\(\),]')
    filtered = filter(dropPat.match, stringList)
    filtered = [parenPat.sub(' ',a) for a in filtered]
    return map(string.strip,filtered)

def readData(fileName, cols, nCol=1):
    return loadArray(fileName,usecols=cols, unpack=True)

def vmag(U):
    d0,d1=U.shape
    if d1>1:
        out = numpy.zeros(d0)
        for i,row in enumerate(U):
            out[i] = numpy.sqrt(numpy.dot(row,row))
        return out

def plotFFT(
            samples,
            sampleFrq,
            filterWidth=1,
            refpower=1000,
            plotref=False,
            plotdata=True,
            log=False):
#    from scipy.signal.signaltools import medfilt

    n=len(samples)

    freq=numpy.array(range(n/2+1))/(n/2.0)
    freq=freq[1:]*sampleFrq/2.0

    if plotdata:
        Y = numpy.fft.fft(samples)
        power = abs(Y[1:(n/2)+1])**2/n
        #power = scipy.signal.signaltools.medfilt(power,filterWidth)
        # TODO: add option to plot powerdensityspectra:
        # pref =2.0e-5
        # power = 10*pylab.log10(power/pref**2)
        # (and plot with semilogy)
        if log:
            pylab.loglog(freq,power)
        else:
            pylab.plot(freq,power)
    if plotref:
        kappa53 = pow(freq,-5./3)*refpower
        if log:
            pylab.loglog(freq,kappa53) 
        else:
            pass
    return 

def getNVectors(anarray):
    if anarray.ndim == 1:
        return 1
    else:
        return anarray.shape[0]

def main():
    arguments = getArgs()
    fileName = arguments['file']
    samplFrq = arguments['f']
    refline = arguments['plotref']
    if arguments['ncol'] > 1:
        print "Multi column data not implemented!"
        #sys.exit(1)

    sampleVectors = readData(fileName,arguments['col'])

    # Since pylab.load (called from loadArray) is used to read
    # data, it becomes one vector if only one column is used
    # or an array of vectors if more columns are used. Have to
    # find out how data is stored in sampleVectors.
    nVectors = getNVectors(sampleVectors)

    legend = map(str,arguments['col'])
    if refline:
        legend.append('k^-5/3')
    
    for i in  range(nVectors):
        print 'Processing sample vector',i
        currentVector = []
        if nVectors == 1:
            currentVector = sampleVectors
        else:
            currentVector = sampleVectors[i]
 
        plotFFT(currentVector, \
                samplFrq, \
                filterWidth=arguments['fwidth'], \
                plotref=False, \
                log=arguments['log']) 
    plotFFT(currentVector, \
            samplFrq, \
            filterWidth=arguments['fwidth'], \
            plotdata=False, \
            refpower=arguments['refpower'], \
            plotref=refline, \
            log=arguments['log'])
    
    pylab.grid()
    
    pylab.title(fileName)
    pylab.legend(legend)
    pylab.xlabel('frequency (Hz)')
    
    if arguments['image']:
        pylab.savefig(arguments['image'])
    pylab.show()


def testRead():
    arguments = getArgs()
    fileName = arguments['file']
    samplFrq = arguments['f']
    refline = arguments['plotref']
    sampleVectors = readData(fileName,arguments['col'],arguments['ncol'])
    print len(sampleVectors.shape)
    for i in range(len(sampleVectors.shape)):
        print sampleVectors[i]
        print sampleVectors[i].__class__
 

if __name__ == "__main__":
    #testRead()
    main()

