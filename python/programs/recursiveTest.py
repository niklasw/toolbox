#!/usr/bin/env python

import os

dirStartTag = "<dir>"
dirEndTag = "</dir>"
fileStartTag = "<file>"
fileEndTag = "</file>"

def extractDirs(flist):
    extracted = []
    for file in flist:
        if os.path.isdir(file):
            extracted.append(file)
    return extracted


def walk(indent):
    cwd = os.getcwd()
    fileList = os.listdir(cwd)
    dirList = extractDirs(fileList)
    for dir in dirList:
        os.chdir(dir)
        indent += '   '
        print indent,dirStartTag,'\n',indent,indent,cwd
        walk(indent)
        print indent,dirEndTag
        indent = indent[0:len(indent)-3]
        os.chdir('..')
    return

if __name__=='__main__':
    indent = ''
    walk(indent)

