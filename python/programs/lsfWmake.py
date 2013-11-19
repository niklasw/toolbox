#!/usr/bin/env python

import string, os, re, sys

class JobFile:
    def __init__(self,**kwargs):
        self.__dict__.update(locals()['kwargs'])

    def template(self):
        return ''

    def asString(self):
        template = string.Template(self.template())
        bsubFile = template.substitute(module=self.module,
                   cwd=os.getcwd(), np=self.np,
                   queue=self.queue, exe=self.exe)
        return bsubFile

    def write(self, fileName):
        with open(fileName,'w') as fh:
            fh.write(self.asString())

    def __str__(self):
        return self.asString()


class pbsJobFile(JobFile):
    def __init__(self,**kwargs):
        JobFile.__init__(self,**kwargs)
        self.__dict__.update(locals()['kwargs'])

    def template(self):
        print 'NOT IMPLEMENTED'
        sys.exit(1)

class lsfJobFile(JobFile):
    def __init__(self,**kwargs):
        JobFile.__init__(self,**kwargs)
        self.__dict__.update(locals()['kwargs'])

    def template(self):
        s='''#!/bin/bash
module add $module
foam
#BSUB -cwd "$cwd"
#BSUB -J "$exe"
#BSUB -n $np
#BSUB -q $queue
#BSUB -x
export WM_NCOMPPROCS="$$LSB_DJOB_NUMPROC"
$exe >& $exe.log
'''
        return s

def submit(cmd=['bsub'],jobFileString=''):
    from subprocess import Popen,PIPE
    import re
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process.stdin.write(jobFileString)
    out,err = process.communicate()

    match = re.search('.*<([0-9]+)>.*',out)
    if match:
        print match.group(1)
    else:
        print('Job submission failed with output\n%s\n%s\n' % (out,err))


if __name__=='__main__':
    qsys= 'lsf'

    submitCmds = {'lsf':['bsub'], 'pbs':['qsub']}

    args = {'module':'openfoam/2.1.x', 'exe':'wmake', 'queue':'debug', 'np': 12}

    f = (lsfJobFile if qsys == 'lsf' else pbsJobFile)(**args)
    print f
    submit(submitCmds[qsys],f.asString())




