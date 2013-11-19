#!/usr/bin/python

mjol=2.5/2
salt=0.5/2*5.0
mjolk=6.0/2
egg=1.
smor=50/2.0
nLaggs=10/2.0

import sys
try:
    naggs=int(sys.argv[1])
except:
    print 'Supply numner of eggs (integer) as argument'
    sys.exit(1)

print 'Till ca %3i laggar\n================' % (int(round(nLaggs*naggs)))
print 'Vetemjol %3.1f dl' % (mjol*naggs)
print 'Mjolk    %3.1f dl' % (mjolk*naggs)
print 'Salt     %3.1f ml' % (salt*naggs)
print 'Agg      %3i st' % (naggs)
print 'Smor     %3i g' % (smor*naggs)


