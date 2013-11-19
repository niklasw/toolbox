#!/usr/bin/env python

import os,re,sys

def checkargs(args):
    nargs = len(args)
    if nargs != 3 or re.match(r'^-+h',args[1]):
        print "Usage:",os.path.basename(args[0]),"<fileRoot> <fileEnd>"
        sys.exit(1)
    return args[1:]

def getfiles(root,tail):
    flist = []
    for file in os.listdir(os.getcwd()):
        if re.match(root,file) and re.search(tail,file):
            flist.append(file)
    return flist

def padWithZeroes(flist,root,tail):
    for file in flist:
        num = file.split(root)[1]
        num = num.split(tail)[0]
        num = num.zfill(7)
        newfile = root+num+tail
        os.rename(file,newfile)
        print file,"\t->\t",newfile

def main():
    root,tail = checkargs(sys.argv)

    flist = getfiles(root,tail)

    padWithZeroes(flist,root,tail)

if __name__=="__main__":
    main()

