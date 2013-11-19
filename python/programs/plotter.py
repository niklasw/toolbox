#!/usr/bin/python

import os,sys,re


prog=os.path.basename(sys.argv[0])

class plotMaker:
    def __init__(self, options):
        from pylab import *
        import scipy
        self.data=[]
        self.files=[]
        self.legendNames=[]
        self.dosave=False
        self.dolog=False
        self.doclean=False
        self.doshow=True
        self.figname='plot.png'
        self.tempfile='/tmp/plotData.tmp'
        self.usecols="0:1"

    def parseArgs(self):
        args=self.options
        args.reverse()
        args.pop()
        while len(args):
            arg=args.pop()
            if os.path.isfile(arg):
                self.files.append(arg)
            elif arg=='-log':
                self.dolog=True
            elif arg=='-legend':
                self.legendNames=self.getnext(args).split()
            elif arg=='-grid':
                grid()
            elif arg=='-save':
                self.dosave=True
                self.figname=self.getnext(args)
            elif arg=='-x':
                self.xlabel(self.getnext(args))
            elif arg=='-y':
                self.ylabel(self.getnext(args))
            elif arg=='-title':
                self.title(self.getnext(args))
            elif arg=='-noshow':
                self.doshow=False
            elif arg=='-clean':
                self.doclean=True
            elif arg=='-use':
                self.usecols=self.getnext(args)
            else:
                print 'Uknown argument', arg, '\n'
                self.usage(True)

    def usage(self,exit):
        print """
        Python thing relying on pylab and scipy to plot
        column stored data in one or several files. Data
        files can contain one or two columns.
        
        Usage: plot0.py <file> [file2 [file3]] [options]
        
        Options are:
        -log                Log Y axis
        -legend "a b c"     Adds a legend
        -grid
        -save fig.png       Outputs result to disk
        -title Title        Adds Title to plot
        -x                  X axis label
        -y                  Y axis label
        -noshow             Silent mode, no plot window
        -use                Columns to use 1:2
        -clean              Try to clean up file from
                            text headers etc
        """
        sys.exit(1)

    def getNext(self,alist):
        try:
            astring=alist.pop()
            if astring[0] == '-':
                print "Syntax error in argument list near:",astring
                sys.exit(1)
            return astring
        except:
            return "Error"

    def cleanFile(self,infile,outfile):
        import fileinput,re
        pat=re.compile(r'[a-df-zA-DF-Z"]')
        tmpfile=open(outfile,'w')
        for line in fileinput.input(infile):
            if not pat.search(line):
                tmpfile.write(line)

    def getCols(self,astring):
        cols=astring.split(':')
        return len(cols), [ int(a) for a in cols ]

    def readData(self):
        for file in files

for file in files:
    if doclean:
        cleanfile(file,tempfile)
        file=tempfile
    try:
        data.append(load(file))
    except:
        print "Could not load",file,"\nExiting.\n"
        sys.exit(1)

for d in data:
    d=scipy.array(d)
    ashape=shape(d)
    print 'Data array shape:',ashape
    nrows=ashape[0]
    ncols = 1
    x=y=array(0)
    Y=[]
    if size(ashape)>1:
        ncols = ashape[1]
    if ncols>1:
        ncols,cols=getcols(usecols)
        print cols
        x=d[:,cols[0]]
        for i in range(ncols-1):
            y=d[:,cols[i+1]]
            Y.append(y)
    else:
        x=linspace(0,nrows-1,nrows)
        y=d[:]

    if dolog:
        print "WARNING:\nEvaluating magnitude of variable to avoid log(-y)"
        for y_ in Y:
            semilogy(x,fabs(y_))
    else:
        for y_ in Y:
            plot(x,y_,'o-')

if len(legendNames)>0:
    legend(legendNames)
if dosave:
    savefig(figname)
    print "Saved residual plot image in",figname
if doshow:
    show()
