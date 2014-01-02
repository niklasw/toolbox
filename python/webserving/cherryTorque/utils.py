#!/usr/bin/python

def Error(s,sig=1):
    import sys
    print '\nError %s!\n' % s
    sys.exit(sig)

def Warn(s):
    output = 'Warning %s!' % s
    print '\n'+'='*len(output)
    print output
    print '='*len(output)

def Info(s):
    print '\t%s' % s

def hms2s(hmsString,sep=':'):
    from operator import mul
    hms = map(int,hmsString.split(sep))
    return sum(map(mul,hms,(3600,60,1)))

def s2hms(s,sep=':'):
    H,S=int(s/3600),s%3600
    M,S=int(S/60),S%60
    return sep.join( [ '{0:02d}'.format(i) for i in [H,M,S] ] )

def date2epoch(d,fmt='%Y-%m'):
    import time
    return time.mktime(time.strptime(d,fmt))

def epoch2date(e,fmt='%Y-%m'):
    import time
    return time.ctime(e)

def coreCount(ppnString):
    n,ppn = ppnString.split(':',1)
    nNodes = int(n)
    nCores = int(ppn.split('=')[-1])
    return nNodes*nCores

# Perf timer
def timeit(method):
    import time
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        Info('Function performance: %r (%r, %r) %2.2f sec' %  (method.__name__, args, kw, te-ts))
        return result

    return timed
