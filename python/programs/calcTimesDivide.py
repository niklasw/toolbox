#!/usr/bin/env python

import sys,re,math,string

arg0 = sys.argv[0].split('/')[-1]

def hmscheck(hmsString,sep=':'):
    pat=re.compile(r'(\d+:?){1,3}$')
    if not pat.match(hmsString):
        print 'Time string format error in',hmsString
        return ''
    return hmsString

def hms2s(hmsString,sep=':'):
    hms = []; secs=0
    hms = [ int(i) for i in hmsString.split(':') ]
    try:
        secs= {
         1: lambda hms: hms[0]*3600,
         2: lambda hms: hms[0]*3600+hms[1]*60,
         3: lambda hms: hms[0]*3600+hms[1]*60+hms[2]}[len(hms)](hms)
    except KeyError:
        print 'format error\n'
        main()

    return secs
    
def s2hms(s,sep=':'):
    h = s/3600
    m = (s-h*3600)/60
    s = s-h*3600-m*60
    h,m,s = [ str(i) for i in [h,m,s] ]
    return h+sep+m+sep+s

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
    dts = hms2s(hms1)*1.0/hms2s(hms2)
    print 'Time quote is:',dts
    return

main()

