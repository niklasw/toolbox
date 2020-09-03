#!/usr/bin/python

mjol=4.5/3
salt=2.0/3
mjolk=6.5/3
egg=1.
smor=50/3.0
nLaggs=10/3.0

import sys
try:
    naggs=int(sys.argv[1])
except:
    print('Supply numner of eggs (integer) as argument')
    sys.exit(1)

print('Till ca %3i laggar\n================' % (int(round(nLaggs*naggs))))
print('Vetemjol %3.1f dl' % (mjol*naggs))
print('Mjolk    %3.1f dl' % (mjolk*naggs))
print('Salt     %3.1f ml' % (salt*naggs))
print('Agg      %3i st' % (naggs))
print('Smor     %3i g' % (smor*naggs))


