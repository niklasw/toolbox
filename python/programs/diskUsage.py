#!/usr/bin/env python3

from subprocess import Popen,PIPE
import os,sys,string


if not os.getuid() == 0:
    print('Note: You will obviously only see what you have permission to read.')
    print('-------------------------------------------------------------------')
    print('')

root=os.getcwd()
if len(sys.argv) == 2:
    d=sys.argv[1]
    root=os.path.join(root,d)
    if not os.path.isdir(root):
        print('Cannot find directory {0}.'.format(root))
        sys.exit(1)

print('Parsing directories under {0}'.format(root))

dirs=[os.path.join(root,d) for d in os.listdir(root)]

if not dirs:
    print('No files found')
    sys.exit(0)

# Du will be reported in kiloBytes
cmnd= ['du', '-sck']+dirs

p = Popen(cmnd,stdout=PIPE,stderr=PIPE)

out,err = p.communicate()

dirs={}
for line in out.split('\n'.encode()):
    try:
        du,dir = line.split(maxsplit=1)
        dirs[int(du)] = dir
    except:
        continue

for du in sorted(iter(dirs.keys()),reverse=True):
    if du > 1024**2:
        unit = 'G'
        size = du/1024.0**2
    elif du > 1024:
        unit = 'M'
        size = du/1024.0
    else:
        unit = 'K'
        size = du
    print("%7.1f %s %s"%(size,unit, dirs[du]))
