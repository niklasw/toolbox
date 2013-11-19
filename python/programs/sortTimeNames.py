#!/usr/bin/python

import os,sys

def folderlist(apath):
    fl=os.listdir(apath)
    folders=[]
    for f in fl:
        if os.path.isdir(os.path.join(apath,f)):
            folders.append(f)
    return folders

def numericnames(alist):
    numbers=[]
    for a in alist:
        try:
            tmp=float(a)
            numbers.append(a)
        except:
            print '\tnumericnames() rejecting',a
    return numbers

def atof(alist):
    try:
        return [float(a) for a in alist]
    except:
        print """
            ERROR in sortTimeNames.py atof():
            unfloatable string in arglist""",alist
        return []

def sorttimefolders(apath):
    folders=folderlist(apath)
    timenames=numericnames(folders)
    sortednames=sorted(map(float,timenames))
    return sortednames

if __name__=='__main__':
    cwd=os.getcwd()
    if len(sys.argv)==2:
        cwd=sys.argv[1]
    print sorttimefolders(cwd)


