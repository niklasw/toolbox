#!/usr/bin/env python2

import sys,re,math,string

arg0 = sys.argv[0].split('/')[-1]

def hmscheck(hmsString,sep=':'):
    pat=re.compile(r'(\d+:?){1,3}$')
    if not pat.match(hmsString):
        print 'Time string format error in',hmsString
        return ''
    return hmsString

def hms2s(hmsString,sep=':'):
    from operator import mul
    hms = map(int,hmsString.split(sep))
    try:
        return sum(map(mul,hms,(3600,60,1)))
    except KeyError:
        print 'format error\n'
        main()

def s2hms(s,sep=':'):
    H,S=int(s/3600),s%3600
    M,S=int(S/60),S%60
    return sep.join( [ '{0:02d}'.format(i) for i in [H,M,S] ] )

def dTime(hms1,hms2,sep=':'):
    return s2hms(hms2s(hms2,sep)-hms2s(hms1,sep),sep)

def printHelp(name):
    print '\nCalculates time between two instances on h:m:s format.'
    print 'Usage:'
    print '  ',name,'[start time] [end time] Or just',name,'\n'

def main():
    argv=sys.argv
    if len(argv) == 1:
        hms1=hms2=''
        while not hms1:
            print 'Input start time [hh:mm:ss]: '
            hms1 = hmscheck(sys.stdin.readline())
        while not hms2:
            print 'Input end time [hh:mm:ss]: '
            hms2 = hmscheck(sys.stdin.readline())
    elif len(argv) == 3:
        hms1=hmscheck(argv[1])
        hms2=hmscheck(argv[2])
        if not hms1 or not hms2:
            return
    else:
        printHelp(arg0)
        return
    dts = hms2s(hms2)-hms2s(hms1)
    if dts < 0:
        print 'Warning: End time earlier than start time, assuming yesterday!'
        dts = hms2s(hms2)+hms2s('24')-hms2s(hms1)
    dthms = s2hms(dts)
    print 'Time gap is:',dthms
    print '('+str(dts),'seconds)\n'
    return

main()

