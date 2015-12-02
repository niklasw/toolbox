#!/usr/bin/env python

import os,sys,re
import string
try:
    import numpy
    import matplotlib.pyplot as plt
except:
    print 'Python modules numpy and and matplotlib must be installed to run this script'
    sys.exit(1)


prog=os.path.basename(sys.argv[0])


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
    Python thing to simply plot data
    """

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print '\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*')
        parser.print_help()
        sys.exit(1)

    def validateFiles(args):
        if not args:
            argError('Input data file needed.')
        for f in args:
            if not os.path.isfile(f):
                argError('Cannot read file {0}'.format(f))

    def validateOption(option, test, msg='Invalid argument', allowed=[]):
        try:    option = test(option)
        except: argError('%s; got %s' % (msg,option))
        if allowed and not option in allowed:
            argError('%s; got %s. Allowed values are %s' % (msg,option,allowed))
        return option

    parser=OptionParser(description=descString)
    parser.add_option('--negX',dest='negX',action='store_true',default=False,help='Negate X-values')
    parser.add_option('--negY',dest='negY',action='store_true',default=False,help='Negate Y-values')
    parser.add_option('--translateX',dest='translateX',default=0.0,help='Translate X-values')
    parser.add_option('--translateY',dest='translateY',default=0.0,help='Translate Y-values')
    parser.add_option('--scaleX',dest='scaleX',default=1.0,help='scale X-values')
    parser.add_option('--scaleY',dest='scaleY',default=1.0,help='scale Y-values')
    parser.add_option('--logX',dest='logX',action='store_true',default=False,help='Log X axis')
    parser.add_option('--logY',dest='logY',action='store_true',default=False,help='Log Y axis')
    parser.add_option('--diff',dest='diff',action='store_true',default=False,help='Plot diff of Y values instead')
    parser.add_option('--filter',dest='filterWidth',default=0,help='Filter Y-data with this filter width')
    parser.add_option('--skipLines',dest='skipLines',default=0,help='Number of data lines to skip')

    parser.add_option('-x','--xLabel',dest='xLabel',default='x',help='X axis label')
    parser.add_option('-y','--yLabel',dest='yLabel',default='y',help='Y axis label')
    parser.add_option('-g','--grid',dest='grid',action='store_true',default=False,help='Canvas grid')
    parser.add_option('--square',dest='square',action='store_true',default=False,help='Force axis equal')
    parser.add_option('--noShow',dest='noShow',action='store_true',default=False,help='Do not open plot window')
    parser.add_option('-s','--save',dest='figName',default='',help='Save plot to this image file')
    parser.add_option('-t','--title',dest='title',default='',help='Plot title')
    parser.add_option('-L','--legend',dest='legend',default='',help='Legend definition. Colon separated strings')
    parser.add_option('-l','--lineStyle',dest='lineStyle',default='-',help='Line style e.g. "-o"')

    parser.add_option('--xMin', dest='xMin',default=False, help='X-axis lower limit')
    parser.add_option('--xMax', dest='xMax',default=False, help='X-axis upper limit')
    parser.add_option('--yMin', dest='yMin',default=False, help='Y-axis upper limit')
    parser.add_option('--yMax', dest='yMax',default=False, help='Y-axis upper limit')

    parser.add_option('-c','--use',dest='columns',default='0:1',help='Define columns to plot e.g. 0:1:3')

    parser.add_option('-F','--fft',dest='fft', default=0, help = 'Also plot fft on dataset, argument is dt. 0 disables fft.')

    options,arguments = parser.parse_args()

    validateFiles(arguments)

    options.translateX  = validateOption(options.translateX,float)
    options.translateY  = validateOption(options.translateY,float)
    options.scaleX      = validateOption(options.scaleX,float)
    options.scaleY      = validateOption(options.scaleY,float)
    options.filterWidth = validateOption(options.filterWidth,int)
    options.xMin        = validateOption(options.xMin,float)
    options.xMax        = validateOption(options.xMax,float)
    options.yMin        = validateOption(options.yMin,float)
    options.yMax        = validateOption(options.yMax,float)
    options.skipLines   = validateOption(options.skipLines,int)
    options.fft         = validateOption(options.fft,float)

    return options,arguments

class dataManager:
    dropPat = re.compile('^\s*(?![\(\)\#"\/a-zA-Z])')
    parenPat = re.compile('[,\(\)]')

    def __init__(self, options, files):
        self.options = options
        self.files = files
        self.arrays = []
        self.shapes = []
        self.current = 0
        self.legend = []
        self.optionsApplied = []
        self.fft = None
        self.fftFrq = None

    def getCols(self):
        cols=self.options.columns.split(':')
        return len(cols), [ int(a) for a in cols ]

    def getLegend(self):
        if self.options.legend:
            self.legend = self.options.legend.split()

    def meanFilter(self,A,i,w):
        hw = int(w/2)
        w0 = min(hw,max(i-hw,0))
        w1 = max(hw,min(hw,len(A)-i))
        return numpy.mean(A[i-w0:i+w1])

    def filtered(self,A,w):
        return numpy.array( [ self.meanFilter(A,i,w) for i in range(len(A)) ])

    def clean(self,stringList):
        from itertools import ifilter
        return (self.parenPat.sub(' ',a).strip() for a in ifilter(self.dropPat.match,stringList))

    def read(self):
        from itertools import imap

        for f in self.files:
            Info( 'Reading file {0}'.format(f))
            fLList=[]
            with open(f) as fp:
                for i,line in enumerate(self.clean(fp.readlines())):
                    if i >=  self.options.skipLines:
                        try:
                            fLList.append(map(float,line.split()))
                        except:
                            print "Warning: Could not read line number {0}".format(i)

            if not len(fLList):
                Warn('skipLines > data set length. Data set ignored')
                continue

            fLList=filter(len,fLList)

            try:
                self.arrays.append(numpy.asarray(fLList))
                self.shapes.append(numpy.shape(self.arrays[-1]))
                self.current += 1
            except:
                Warn('Could not load {0}. Skipping data set.'.format(f))

    def shape(self):
        return self.shapes[self.current]

    def extractXY(self):
        d = self.arrays[self.current]
        nRows = self.shape()[0]
        nCols, cols = self.getCols()

        self.y = []
        if nCols == 1:
            self.x = numpy.arange(0,nRows,1)
            self.y.append(d[:,0])
        else:
            self.x = d[:,cols[0]]
            for c in range(1,nCols):
                self.y.append(d[:,cols[c]])

        self.optionsApplied.append(False)


    def assertXY(self):
        self.extractXY()
        for y in self.y:
            if not len(self.x) == len(y):
                Error('Assertion error. Column length mismatch: X = {0}, Y = {1}'.format(len(self.x),len(y)))
            else:
                Info('Number of data points {0}, {1}'.format(len(self.x),len(y)))

    def assertLegend(self):
        self.getLegend()
        if self.legend:
            if not len(self.legend) == len(self.y):
                Warn('Legend assertion error. Legend does not match data and is disabled')
                return False
        return True

    def diff(self,x,y):
        dx = (x[1:]-x[0:-1])
        dy = (y[1:]-y[0:-1])
        return dy/dx

    def FFT(self,dt):
        import scipy
        self.fft = []
        self.fftFrq = []
        dt = self.options.fft
        for y in self.y:
            n = len(self.y)
            sampleFrq = 1.0/dt
            freq = numpy.array(range(n/2+1))/(n/2.0)
            y = freq[1:]*sampleFrq/2.0
            power = scipy.fft(self.y)
            self.fft.append(abs(y[1:(n/2)+1])**2/n)
            self.fftFrq.append(freq)

    def applyDataOptions(self):
        if not self.optionsApplied[self.current]:
            Info('Applying data transformations')

            if self.options.filterWidth:
                for i,y in enumerate(self.y):
                    self.y[i] = self.filtered(y, self.options.filterWidth)

            self.x *= self.options.scaleX
            self.x += self.options.translateX

            if self.options.diff:
                for i,y in enumerate(self.y):
                    self.y[i] = self.diff(self.x,y)
                self.x = (self.x[1:]+self.x[0:-1])*0.5

            for i,y in enumerate(self.y):
                y *= self.options.scaleY
                y += self.options.translateY

                if self.options.logY:
                    Warn('Negative y-values are zeroed due to log option')
                    self.y[i] = numpy.log(numpy.maximum(y,0))

            if self.options.logX:
                Warn('Negative x-values are zeroed due to log option')
                self.x = numpy.log(numpy.maximum(self.x,0))

            if self.options.fft != 0:
                self.FFT(5e-4)

            self.optionsApplied[self.current] = True

    def nArrays(self):
        return len(self.arrays)


class plotter:
    lineColors='b r g c m y k'.split()
    def __init__(self, dmgr):

        self.data=dmgr
        self.lines = []
        self.fftLines = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111) #,**axesKw)

    def add(self):
        for i,d in enumerate(self.data.y):
            line, = plt.plot(self.data.x,d,
                             color=self.lineColors[i],
                             #color=self.lineColors[self.data.current],
                             linestyle=self.data.options.lineStyle)
            self.lines.append(line)

            print 'Average of data set {0} = {1}'.format(i,sum(d)/len(d))


    def addFft(self):
        if not self.data.fft:
            return

        self.fftFig = plt.figure()
        self.fftAx  = self.fftFig.add_subplot(111)
        for i,d in enumerate(self.data.fft):
            x = self.fftFrq[i]
            line, = plt.loglog(x,d,
                               self.lineColors[i],
                               linestyle=self.data.options.lineStyle)
            self.fftLines.append(line)

    def decorate(self):
        '''Legend is defined by the last data set (loaded file)
        '''
        xmin,xmax=plt.xlim()
        if self.data.options.xLabel:
            self.ax.set_xlabel(self.data.options.xLabel)
        if self.data.options.yLabel:
            self.ax.set_ylabel(self.data.options.yLabel)
        if self.data.options.grid:
            self.ax.grid('on')
        if self.data.options.title:
            self.ax.set_title(self.data.options.title)
        if self.data.legend and self.data.assertLegend():
            self.ax.legend(self.lines,self.data.legend, loc=0)

        if self.data.options.yMin:
            ymin=self.data.options.yMin
            plt.ylim(ymin,plt.ylim()[1])
        if self.data.options.yMax:
            ymax=self.data.options.yMax
            plt.ylim(plt.ylim()[0],ymax)
        if self.data.options.xMin:
            xmin=self.data.options.xMin
            plt.xlim(xmin,xmax)
        if self.data.options.xMax:
            xmax=self.data.options.xMax
            plt.xlim(xmin,xmax)

        if self.data.options.square:
            self.ax.set_aspect('equal')

    def save(self):
        if self.data.options.figName:
            self.fig.savefig(self.data.options.figName)
            Info('Plot saved to image {0}'.format(self.data.options.figName))


    def show(self):
        if self.data.options.noShow:
            return
        else:
            plt.show(block=True)

if __name__=="__main__":
    opt,arg = getArgs()

    data = dataManager(opt,arg)
    data.read()

    p = plotter(data)

    for i in range(data.nArrays()):
        data.current = i
        data.assertXY()
        data.applyDataOptions()
        p.add()

    p.decorate()
    p.save()
    p.show()

