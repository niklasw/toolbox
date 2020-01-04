#!/usr/bin/env python

import os,sys,re
from fileParsing import *
import string
try:
    import pylab
except:
    print 'Python modules pylab and numpy must be installed to run this script'
    sys.exit(1)


prog=os.path.basename(sys.argv[0])

def getnext(alist):
    try:
        astring=alist.pop()
        if astring[0] == '-':
            print "Warning minus sign in argument list near:",astring
            #sys.exit(1)
        return astring
    except:
        return "Error"

def getpart(infile,bpat,epat):
    fp=open(infile,'r')
    data,hdr=readBetween(fp,bpat,epat,1,'')
    return data.split('\n')

def cleanData(stringList):
    dropPat = re.compile('^\s*(?![\(\)\#"\/a-zA-Z])')
    parenPat = re.compile('[,\(\)]')
    filtered = filter(dropPat.match, stringList)
    filtered = [parenPat.sub(' ',a) for a in filtered]
    return map(string.strip,filtered)

def getcols(astring):
    cols=astring.split(':')
    return len(cols), [ int(a) for a in cols ]

def meanFilter(A,i,w):
    hw = int(w/2)
    w0 = min(hw,max(i-hw,0))
    w1 = max(hw,min(hw,len(A)-i))
    return pylab.mean(A[i-w0:i+w1])

def filtered(A,w):
    return pylab.array( [ meanFilter(A,i,w) for i in range(len(A)) ])

def usage(exit):
    print """
    Python thing relying on pylab and numpy to plot
    column stored data in one or several files. Data
    files can contain one or two columns.

    Usage: plot0.py <file> [file2 [file3]] [options and arguments]

    Options are:
    -minus              Reverse sign on Y data
    -log                Log Y axis
    -diff               Plot the diff of data instead
    -filter [width]     mean filter data with filter width
                        width must be even
    -legend "a b c"     Adds a legend
    -legendloc [0-10]   Legend location (pydoc pylab.legend)
    -grid
    -square             Does axis(equal)
    -linestyle "r-o"
    -save fig.png       Outputs result to disk
    -title Title        Adds Title to plot
    -xlim               X axis limits min max
    -ylim               y axis limits min max
    -x                  X axis label
    -y                  Y axis label
    -normalize          (scalar)
    -normalizex         (scalar)
    -trx                Translate along x
    -try                Translate along y
    -noshow             Silent mode, no plot window
    -use                Columns to use 1:2
    -clean              Try to clean up file from
                        text headers etc
    -fromto "start pattern" "end pattern"
                        Plot only lines between
                        regexp patterns
    """
    sys.exit(1)

arguments=sys.argv[:]
prog=arguments[0]
data=[]
files=[]
legendNames=[]
legendLocation=0
dosave=False
dolog=False
linlog=False
dodiff=False
filterWidth=0
doclean=False
doshow=True
linestyle=''
figname='plot.png'
tempfile='/tmp/plotData.tmp'
usecols="0:1"
bpat=''
epat=''
minus=False
minx=False
maxx=False
miny=False
maxy=False
norm=1
normx=1
translateX=0
translateY=0

arguments.reverse()
arguments.pop()

if not len(arguments):
    usage(True)
while len(arguments):
    arg=arguments.pop()
    if os.path.isfile(arg):
        files.append(arg)
    elif arg=='-minus':
        minus=True
    elif arg=='-normalize':
        norm=float(getnext(arguments))
    elif arg=='-normalizex':
        normx=float(getnext(arguments))
    elif arg=='-trx':
        argument = getnext(arguments)
        print(argument)
        translateX=float(argument)
    elif arg=='-try':
        argument = getnext(arguments)
        print(argument)
        translateY=float(argument)
    elif arg=='-linlog':
        linlog=True
    elif arg=='-log':
        dolog=True
    elif arg=='-diff':
        dodiff=True
    elif arg=='-filter':
        filterWidth=int(getnext(arguments))
    elif arg=='-legendloc':
        legendLocation=getnext(arguments).split()
    elif arg=='-legend':
        legendNames=getnext(arguments).split()
    elif arg=='-linestyle':
        linestyle=getnext(arguments)
    elif arg=='-grid':
        pylab.grid()
    elif arg=='-square':
        pylab.axis('equal')
    elif arg=='-save':
        dosave=True
        figname=getnext(arguments)
    elif arg=='-xlim':
        minx = float(getnext(arguments))
        maxx = float(getnext(arguments))
        pylab.xlim(minx,maxx)
    elif arg=='-ylim':
        miny = float(getnext(arguments))
        maxy = float(getnext(arguments))
        pylab.ylim(miny,maxy)
    elif arg=='-x':
        pylab.xlabel(getnext(arguments))
    elif arg=='-y':
        pylab.ylabel(getnext(arguments))
    elif arg=='-title':
        pylab.title(getnext(arguments))
    elif arg=='-noshow':
        doshow=False
    elif arg=='-clean':
        doclean=True
    elif arg=='-use':
        usecols=getnext(arguments)
    elif arg=='-fromto':
        bpat=re.compile(getnext(arguments))
        epat=re.compile(getnext(arguments))
    else:
        print 'Uknown argument', arg, '\n'
        usage(True)

for file in files:
    print "Reading file",file,"\n"
    thisData=''
    if bpat and epat:
        thisData=getpart(file,bpat,epat)
    else:
        thisData=open(file).readlines()
    thisData=cleanData(thisData[:])
    fLList=[]
    for line in thisData:
        try:
            fLList.append(map(float,line.split()))
        except:
            print "Warning: Could not read line", line
    fLList=filter(len,fLList)
    del thisData
    try:
        data.append(pylab.asarray(fLList))
    except:
        print "Could not load",file,"\nExiting.\n"
        sys.exit(1)


for d in data:
    d=pylab.asarray(d)
    ashape=pylab.shape(d)
    print 'Data array shape =',ashape
    nrows=ashape[0]
    ncols = 1
    x=y=pylab.array(0)
    Y=[]
    if pylab.size(ashape)>1:
        ncols = ashape[1]
    if ncols>1:
        ncols,cols=getcols(usecols)
        print "Columns =",cols,", ncols =",ncols
        x=d[:,cols[0]]
        for i in range(ncols-1):
            y=d[:,cols[i+1]]
            Y.append(y)
    else:
        x=pylab.linspace(0,nrows-1,nrows)
        y=d[:]
        Y.append(y)

    for i in range(ncols-1):
        print 'Average of col {0} = {1}'.format(i,sum(Y[i])/len(Y[i]))

    for y_ in Y:
        print 'Plotting'
        y_/=norm
        x+=translateX
        x/=normx
        if minus:
            y_=-y_
        if dodiff:
            y_=pylab.diff(y_)
            x =x[0:-1]
        if dolog:
            print "WARNING:\nEvaluating magnitude of variable to avoid log(-y)"
            y_ = pylab.log10(pylab.fabs(y_))
            x  = pylab.log10(x)
        if linlog:
            y_ = pylab.log10(pylab.fabs(y_))
        if filterWidth:
            y_ = filtered(y_,filterWidth)

        pylab.plot(x,y_,linestyle)
        if miny:
            print 'Using Y axis limits'
            pylab.ylim(miny,maxy)
        if minx:
            print 'Using X axis limits'
            pylab.ylim(minx,maxx)



if len(legendNames)>0:
    pylab.legend(legendNames,loc=legendLocation)
if dosave:
    pylab.savefig(figname)
    print "Saved residual plot image in",figname
if doshow:
    pylab.show()
