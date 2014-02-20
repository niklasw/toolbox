#!/usr/bin/python

import sys
from interactor2 import interactor

def getArgs(i):
    from optparse import OptionParser
    import os
    parser=OptionParser(description="One measure of simulation speed. Can run interactively or parsing a log")
    parser.add_option('-f','--logfile',dest='logfile',default=None, help='Optional log file to parse data from')
    opts,args=parser.parse_args()

    if (getattr(opts, 'logfile')):
        i.info('Will try to parse log for number of steps and clock time.')
        if not os.path.isfile(opts.logfile):
            i.error('Cannot find supplied log file')
        opts.parseLog = True

    return opts, args


def parseLog(logFile):
    from subprocess import Popen,PIPE

    def failed(e):
        print "Log file parsing failed: {0}".format(e)
        sys.exit(1)


    awkCmd='''
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

    cmd = ['awk',awkCmd,logFile]

    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out,err = p.communicate()

    if err:
        failed(err)
    try:
        out = map(int, out.split())
        return out
    except:
        failed('Got this "{0}"'.format(out))

if __name__=='__main__':
    i=interactor()

    opts,args=getArgs(i)

    nCores = i.get('Number of cores', test=int, default=1)
    nCells = i.get('Number of cells', test=float, default=10000)
    cTime = 0
    nSteps= 0
    if not opts.parseLog:
        cTime  = i.get('Elapsed time', test=float, default=1000)
        nSteps = i.get('Number of iterations/time steps', test=int, default=100)
    else:
        nSteps,cTime = parseLog(opts.logfile)

    i.info('\n{0}\n'.format('='*50))
    i.info('Simulation speed index = {0:0.1f} "cell-iterations per core-second".'.format(nSteps*nCells/(nCores*cTime)))

    i.info('')
