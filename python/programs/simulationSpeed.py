#!/usr/bin/python

import sys
from interactor2 import interactor

def getArgs(i):
    from optparse import OptionParser
    import os
    parser=OptionParser(description="One measure of simulation speed. Can run interactively or parsing a log")
    parser.add_option('-f','--logfile',dest='logfile',default=None, help='Optional log file to parse data from')
    parser.add_option('-V','--foamversion',dest='foamversion',default=2, help='Foam version (major only)')
    opts,args=parser.parse_args()

    if (getattr(opts, 'logfile')):
        i.info('Will try to parse log for nProcs, number of steps and clock time.')
        if not os.path.isfile(opts.logfile):
            i.error('Cannot find supplied log file')
        opts.parseLog = True
    else:
        opts.parseLog = False

    return opts, args

def getNCores():
    import os,re
    dirContent=os.listdir(os.getcwd())
    ppat=re.compile('processor[0-9]+')
    return len(filter(ppat.match, dirContent))

def getNCoresFromLog(logFile):
    import re
    pat = re.compile(r'^nProcs\s*:\s*([0-9]+).*$')
    with open(logFile) as log:
        count = 0
        for line in log:
            count+=1
            match = pat.match(line)
            if match:
                return match.group(1)
            if count > 200:
                return 0

def getNCells():
    import re,os
    from os.path import join as pjoin
    from os.path import isfile as isfile
    from glob import glob
    logOpts = glob(pjoin(os.getcwd(),'qlogs','checkMesh*.log'))
    logOpts+= glob(pjoin(os.getcwd(),'logs','checkMesh*.log'))
    logOpts+= glob(pjoin(os.getcwd(),'checkMesh*.log'))

    pat = re.compile(r'cells:\s*([0-9]+)')
    for meshLog in logOpts:
        if isfile(meshLog):
            with open(meshLog,'r') as fp:
                for line in fp:
                    found = pat.search(line)
                    if found:
                        try:
                            nCells = int(found.groups()[0])
                        except:
                            i.info('Failed extracting nCells from log')
                        return nCells
    return 1


def parseLog(opts):
    from subprocess import Popen,PIPE

    def failed(e):
        print "Log file parsing failed: {0}".format(e)
        sys.exit(1)

    # Different awking depending on log file format
    awkCmd1='''
    BEGIN{count=0}
    {
        if ($1 ~ "ClockTime"){
            count++
            ctime=$3
        }
    }
    END{
        printf("%i %i", count, ctime)
    }'''

    awkCmd2='''
    BEGIN{count=0}
    {
        if ($1 ~ "ExecutionTime"){
            count++
            ctime=$7
        }
    }
    END{
        printf("%i %i", count, ctime)
    }'''

    awkCmd = awkCmd2
    if opts.foamversion == "1":
        awkCmd = awkCmd1

    cmd = ['awk',awkCmd,opts.logfile]

    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out,err = p.communicate()

    if err:
        failed(err)
    try:
        out = map(float, out.split())
        for n in out:
            if n <= 0:
                failed('Did you use the version option -V 1?')
        return out
    except:
        failed('Got this "{0}"'.format(out))

if __name__=='__main__':
    i=interactor()

    opts,args=getArgs(i)

    try:
        nCores = int(getNCoresFromLog(opts.logfile))
        i.info('Number of cores from run log = {0}'.format(nCores))
    except:
        nCores = i.get('Number of cores', test=int, default=getNCores())

    try:
        nCells = int(getNCells())
        i.info('Number of cells from mesh log = {0}'.format(nCells))
    except:
        nCells = i.get('Number of cells', test=float, default=getNCells())

    cTime = 0
    nSteps= 0
    if opts.parseLog:
        nSteps,cTime = parseLog(opts)
        i.info('Simulation ran for {0} steps in {1} seconds'.format(nSteps,cTime))
    else:
        cTime  = i.get('Elapsed time', test=float, default=1000)
        nSteps = i.get('Number of iterations/time steps', test=int, default=100)
    i.info('Average core cell count is {0}'.format(float(nCells)/nCores))

    i.info('\n{0}\n'.format('='*50))
    i.info('Simulation  speed index = {0:0.1f} "cell-iterations per core-second".'.format(nSteps*nCells/float(nCores*cTime)))
    i.info('Alternative speed index = {0:0.3e} "core-seconds per cell-iteration".'.format(float(nCores*cTime)/(nSteps*nCells)))

    i.info('')
