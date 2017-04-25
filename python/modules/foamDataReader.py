import numpy,re

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

class Options(dict):
    '''Simple dict wrapper, that might act as the optparse options'''
    def __init__(self,d=None):
        dict.__init__(self,d)
        for key in self:
            setattr(self,key,d[key])

class dataReader:
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


