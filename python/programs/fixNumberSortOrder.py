#!/usr/bin/env python

import re,sys,os,string

version=1.0

def exiting(astring):
    print astring,'\nExiting\n'
    sys.exit(1)

def checkargs(args):
    print '\n',args[0],'version',version
    if len(args)< 4:
        usage="""
        Program to rename numbered files into correct
        alphabetical sort order. E.g. file1.jpg -> file00001.jpg.

        Usage: fixNumSortOrder.py <prefix> <pattern>
        where prefix would be file and pattern file*.jpg in the
        example above.

        Add the flag -renumber if you want to renumber all
        to ensure sequence with unit steps 0000, 0001, 0002
                                                    /nikwik
        """
        exiting(usage)
    return args

args = checkargs(sys.argv)

prefix=args[1]

renumber = False
if '-renumber' in args:
    renumber = True
    args.pop(args.index('-renumber'))

prelen=len(prefix)

prepat=re.compile(prefix)

numpat=re.compile(r'\d+')

files=[]
for ent in args[2:]:
    if os.path.isfile(ent):
        if prepat.match(ent):
            files.append(ent)

count=0
newFiles = []
for file in files:
    tail=file[prelen:]
    num=''
    numatch=numpat.match(tail)
    if numatch:
        count += 1
        num=numatch.group(0)
        numlen=len(num)
        tail=tail[numlen:]
        num=num.zfill(5)
        newname=prefix+num+tail
        newFiles.append(newname)
        os.rename(file,newname)
        print file,'->',newname
print newFiles

if renumber:
    newFiles.sort()
    count = 0
    for file in newFiles:
        tail=file[prelen:]
        num=''
        numatch=numpat.match(tail)
        if numatch:
            num=numatch.group(0)
            numlen=len(num)
            tail=tail[numlen:]
            num = str(count)
            num=num.zfill(5)
            newname=prefix+num+tail
            os.rename(file,newname)
            print file,'->',newname
            count += 1

