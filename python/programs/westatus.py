#!/usr/bin/env python

import os,sys,re,string
from subprocess import Popen,PIPE
from tempfile import mkstemp


userName = os.getenv('USER')

cfdApps=['powerflow','powerflow_disc','openfoam','star','fluent','fire']

tmp1h,tmp1 = mkstemp(suffix='out',prefix='bjobs_',text=True)

def mkBjobCmd(user,app):
    return ['bjobs','-u',user,'-app',app]

def parseOutput(s):
    pat = re.compile('^.*Job <([0-9]+)>,.*BSUB -n\s+([0-9]+).*^',flags=re.M)
    match = pat.search(s)
    if match:
        print match.groups()

p = Popen(mkBjobCmd(userName, 'default'),stdout=PIPE)
out,err = p.communicate()
parseOutput(out)






