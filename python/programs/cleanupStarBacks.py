#!/usr/bin/env python

from subprocess import Popen,PIPE
import os,sys,string
from interactor2 import interactor


if not os.getuid() == 0:
    print 'Note: You will obviously only see what you have permission to read.'
    print '-------------------------------------------------------------------'
    print ''

I = interactor()

cwd = os.getcwd()
login = os.getlogin()
uid = os.getuid()

# Du will be reported in kiloBytes
findCmnd = ['find', cwd, '-iregex', '.*.sim~']
rmCmnd = ['rm','-f']

p = Popen(findCmnd,stdout=PIPE,stderr=PIPE)

out,err = p.communicate()

myBackups=list()
for line in out.split('\n'):
    if os.path.isfile(line):
        file = line
        stat = os.stat(file)
        owner = stat.st_uid
        size = stat.st_size/(1024**2)
        if owner == uid:
            myBackups.append((file,size))

myRemoves=list()
if len(myBackups) > 0:
    I.info('These are your backup files:')
    for item in myBackups:
        I.info('%4i MB\t--- %s' % (item[1],item[0]))

    I.info('Now you will be questioned about the removal of each...')
    for item in myBackups:
        I.info('\n\t> %s' % (item[0]))
        ans = I.yesno('\t>>> Do you want to delete it?')
        if ans:
            myRemoves.append(item[0])
            I.info('Marked for removal: %s' % item[0])

    for item in myRemoves:
        Popen(rmCmnd+[item])
        I.info('Removed %s' % item)

