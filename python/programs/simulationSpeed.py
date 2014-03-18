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
        i.info('Will try to parse log for number of steps and clock time.')
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

    nCores = getNCores() #i.get('Number of cores', test=int, default=1)
    if nCores > 0:
        i.info('Found {0} processor directories. Assuming {0} cores run.'.format(nCores))
    else:
        nCores = 1
        i.info('Warning, found no processor directories.  Assuming serial run.')
    nCells = i.get('Number of cells', test=float, default=10000)
    cTime = 0
    nSteps= 0
    if opts.parseLog:
        nSteps,cTime = parseLog(opts)
        i.info('Simulation ran for {0} steps in {1} seconds'.format(nSteps,cTime))
    else:
        cTime  = i.get('Elapsed time', test=float, default=1000)
        nSteps = i.get('Number of iterations/time steps', test=int, default=100)

    i.info('\n{0}\n'.format('='*50))
    i.info('Simulation  speed index = {0:0.1f} "cell-iterations per core-second".'.format(nSteps*nCells/float(nCores*cTime)))
    i.info('Alternative speed index = {0:0.3e} "core-seconds per cell-iteration".'.format(float(nCores*cTime)/(nSteps*nCells)))

    i.info('')
