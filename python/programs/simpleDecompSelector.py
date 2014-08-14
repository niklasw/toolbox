#!/usr/bin/python

import math,sys

try:
    nProcs = int(sys.argv[1])
except:
    print "\tNeed integer argument!"
    sys.exit(1)

componentMax = 30+1

alternatives = list()

start = 1
while not alternatives:
    for i in range(start,componentMax):
        for j in range(start,componentMax):
            ij = i*j
            for k in range(start,componentMax):
                np = ij*k
                if np == nProcs:
                    if not alternatives:
                        alternatives = [(i,j,k)]
                    else:
                        alternatives.append((i,j,k))
    componentMax = min(componentMax+1,nProcs)
    if componentMax == nProcs: break
    print 'searching...'

if not alternatives:
    print '\tCant do that with {0}. Limited to components < {1}'.format(nProcs,componentMax)
    print 'try:\tn\t({0[0]} {0[1]} {0[2]});'.format((nProcs,1,1))
    sys.exit(0)

avg = lambda x: sum(x) * 1.0 / len(x)
var = lambda x: map(lambda y: (y - avg(x)) ** 2, x)
std = lambda x: math.sqrt(avg(var(x)))

# Select the alternative with
# least standard deviation
minStd = 1000.0
preferred = tuple()
for item in alternatives:
    thisStd = std(item)
    if thisStd < minStd:
        minStd = thisStd
        preferred = item

print '\tn\t({0[0]} {0[1]} {0[2]});'.format(preferred)


