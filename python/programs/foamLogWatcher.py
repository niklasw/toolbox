#!/usr/bin/env python

import re,os,sys
try:
    from pylab import *
except:
    print('Python modules pylab and scipy must be installed to run this script')
    print('On an ubuntu system:')
    print('sudo aptitude install python-scipy python-matplotlib ipython')
    sys.exit(1)


class argumentsCollector: # NOT USED
    def __init__(self):
        from optparse import OptionParser
        self.description = 'Python thing to plot foam log info (residuals, so far)'
        (self.opt, self.arg) = self.parse()
        self.checkOptions()

    def parse(self):
        parser=OptionParser(description=self.description)
        parser.add_option('-f','--file',dest='stlFile',default=None,help='Input stl file')
        parser.add_option('-d','--debug',dest='debug',action='store_true',default=False,help='Enable printout of messages')
        return parser.parse_args()

    def argError(self,s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print('\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*'))
        parser.print_help()
        sys.exit(1)

    def checkOptions(self):
        checkList = [ (o._long_opts[0], o.help)
                      for o in parser.option_list if not o.dest ]


def getArgs():
    from optparse import OptionParser
    descString = """
    Python thing to plot foam log info (residuals, so far)
    """

    parser=OptionParser(description=descString)
    parser.add_option('-f','--file',dest='logFile',default=None,help='Input log file')
    parser.add_option('-d','--debug',dest='debug',action='store_true',default=False,help='Enable printout of messages')

    (opt,arg)=parser.parse_args()

    def argError(s):
        s = '* ERROR: %s. *' % s
        n=len(s)
        print('\n\t%s\n\t%s\n\t%s\n' % (n*'*',s,n*'*'))
        parser.print_help()
        sys.exit(1)

    if not opt.logFile: argError( 'Missing log file argument' )
    if not os.path.isfile(opt.logFile): argError( 'File not found '+ opt.logFile )

    argDict = { 'log':opt.logFile,
                'debug':opt.debug}

    return argDict



class FoamData:
    def __init__(self,debug=False):
        self.patterns = {}
        self.data = {}
        self.floatRexp = '(-?\d+[.]?\d*(e[-+]\d+)?)'
        self.timeRexp = '^.*Time = '+self.floatRexp+'\s*$'
        self.timePat = re.compile(self.timeRexp)
        self.solverLineRexp = '^(.+):\s*Solving for (.+), Initial residual = (.+), Final residual = (.+), No Iterations (.+)$'
        self.continuityLineRexp = '^.*: sum local = (.+), global = (.+), cumulative = (.+)$'
        self.clockLineRexp =  '^ExecutionTime = (.+) s\s+ClockTime = (.+) s.*$'
        self.resMatchGroups = {'solver':1,'variable':2,'initres':3,'finalres':4,'niters':5}
        self.contMatchGroups = {'local':1,'global':2,'cumulative':3}
        self.solverLine = re.compile(self.solverLineRexp)
        self.continuityLine = re.compile(self.continuityLineRexp)
        self.clockLine = re.compile(self.clockLineRexp)
        self.variables = []
        self.data['Time'] = []
        self.debug = debug

    def msg(self,astring):
        if self.debug:
            print(astring)

    def getData(self,lines):
        curVariables = []
        foundSome = False
        for line in lines:
            match = self.timePat.match(line)
            if match: # Hit first line for new time step
                curTime = float(match.group(1))
                self.data['Time'].append(curTime)
                curVariables = []
            else:
                match = self.solverLine.match(line)
                if match:
                    foundSome = True
                    variable = match.group(self.resMatchGroups['variable'])
                    if variable not in self.variables:
                        self.variables.append(variable)
                        self.data[variable] = {'initres':[],'niters':[]}
                    if variable not in curVariables: #Only consider first solver loop in Time
                        curVariables.append(variable)
                        initRes = float(match.group(self.resMatchGroups['initres']))
                        nIters = int(match.group(self.resMatchGroups['niters']))
                        self.data[variable]['initres'].append(initRes)
                        self.data[variable]['niters'].append(nIters)
                else:
                    match = self.continuityLine.match(line)
                    if match:
                        if 'continuity' not in list(self.data.keys()):
                            self.data['continuity']={'local':[],'global':[],'cumulative':[]}
                        for kind in ('local','global','cumulative'):
                            self.data['continuity'][kind].append(float(match.group(self.contMatchGroups[kind])))

        self.msg('\nExtracted data:\n'+str(list(self.data.keys())))
        return foundSome

def dynamicRead(fp, readToRexp=None):
    startPos = fp.tell()
    lastPos = startPos
    if readToRexp:
        lastPat = re.compile(readToRexp)
        line = 'empty'
        while line:
            line = fp.readline()
            if lastPat.match(line):
                lastPos = fp.tell()-len(line)
    fp.seek(startPos)
    if lastPos > startPos:
        return fp.read(lastPos-startPos).strip().split('\n')
    else:
        return ''

class residualPlotter:
    def __init__(self,data,plotNo,logFile,debug=False):
        self.logFile=open(logFile,'r')
        self.lines=[]
        self.labels=[]
        self.axisLimits=[0,1,0,1]
        self.dataContainer = data
        self.data=self.dataContainer.data
        self.plotNo=plotNo
        self.vars=data.variables
        self.times=self.data['Time']
        self.updateInterval = 4
        self.debug=debug
        ion() # Interactive plot mode on

    def msg(self,astring):
        if self.debug:
            print(astring)

    def updateLine(self,X,Y,lineNo=0,bounds=None,lines=None,first=True):
        M = min(len(Y),len(X))
        if first:
            line, = semilogy(X[0:M],Y[0:M])
            lines.append(line)
        else:
            lines[lineNo].set_data(X[0:M],Y[0:M])
        if bounds:
            bounds[0] = min(min(X),bounds[0])
            bounds[1] = max(X)
            bounds[2] = min(min(Y),bounds[2])
            bounds[3] = max(max(Y),bounds[3])
            return bounds

    def drawGraph(self,graphTitle='Residuals'):
        subplot(self.plotNo)
        for var in self.vars:
            self.labels.append(var)
            residual = self.data[var]['initres']
            self.updateLine(self.times,residual,lines=self.lines,first=True)
        axis('auto')
        self.axisLimits = list(axis())
        xlabel('Time')
        title(graphTitle)
        legend(self.labels, loc=3)
        grid()
        draw()
        if self.debug:
            savefig(self.logFile.name+'.png')

    def updateGraphs(self):
        subplot(self.plotNo)
        self.times=self.dataContainer.data['Time']
        for i,var in enumerate(self.vars):
            residual = self.dataContainer.data[var]['initres']
            self.axisLimits = self.updateLine(self.times,residual,
                                              lineNo=i,bounds=self.axisLimits,
                                              lines=self.lines,first=False)
        axis(self.axisLimits)

    def updateData(self, debug=False):
        import time
        while 1: # Wait until there is something to plot
           lines = dynamicRead(self.logFile,readToRexp = self.dataContainer.timePat)
           self.msg('Read %i lines from log file' % len(lines))
           if not self.dataContainer.getData(lines):
               self.msg("No data to plot yet...")
               time.sleep(self.updateInterval/2)
               continue
           else:
               time.sleep(self.updateInterval/2)
               break


    def run(self):
        if not self.debug:
            try:
                pid = os.fork()
                if pid > 0:
                    print('PID =',pid)
                    sys.exit(0)
            except OSError as e:
                    sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
                    sys.exit(1)

        self.updateData()

        self.drawGraph(graphTitle='Residuals. Updated every %s seconds (PID = %i)'% (10, os.getpid()))

        while 1:
            self.updateData()
            self.updateGraphs()


if __name__=='__main__':
    opts = getArgs()
    logFile = opts['log']
    info = opts['debug']
    Data = FoamData(debug=info)
    resPlotter = residualPlotter(Data,111,logFile,debug=info)
    resPlotter.run()


