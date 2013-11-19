#!/usr/bin/env python

import os,sys


class interactor:

    def __init__(self):
        pass

    def error(self,s,sig=1):
        print '\nError %s!\n' % s
        sys.exit(sig)

    def warn(self,s):
        output = 'Warning %s!' % s
        print '\n'+'='*len(output)
        print output
        print '='*len(output)

    def info(self,s):
        print '\t%s' % s

    def fileSelector(self,prompt='Select from above',default='',path='',suffix='*',folder=False):
        import glob
        globbed = glob.glob(os.path.join(path,'*'+suffix))
        if not default: default=globbed[0]

        selectables=[]
        self.info('Selectable files:')
        for f in globbed:
            if os.path.isfile(f):
                f=f.strip()
                selectables.append(f)
                self.info('|--> '+f)
        try:
            selected = raw_input('%s [%s]: '% (prompt,selectables[0])).strip()
            if not selected: selected = selectables[0]
            if not os.path.isfile(selected):
                self.warn('Selection is not a file')
                selected = self.fileSelector(prompt,default,path,suffix,folder)
        except (KeyboardInterrupt,SystemExit):
            self.error('Execution aborted by user')
        return selected

    def get(self,prompt='Enter value',default=10,test=int):
        try:
            selected = raw_input('%s [%s]: '% (prompt,default))
            if not selected: selected = default
            try:
                test(selected)
            except:
                self.warn('Typo: %s is not %s' % (str(selected),test.__name__))
                selected = self.get(prompt,default,test)
        except (KeyboardInterrupt,SystemExit):
            self.error('Execution aborted by user')
        return selected

def removeLines(inString,fromExp,toExp):
    # Remove all lines between and including from and to expressions.
    import re
    lines = iter(inString.split('\n'))
    outString=''
    fromPat = re.compile(fromExp)
    toPat = re.compile(toExp)
    flag = True
    while 1:
        try:
            line = lines.next()
            if fromPat.search(line):
                flag = False
            if toPat.search(line):
                flag = True
                line=lines.next()
            if flag: outString += line+'\n'
        except:
            break
    return outString


if __name__=='__main__':

    i=interactor()

    val=i.get(test=float,default=10)
    sel=i.fileSelector(suffix=".pyc")
    print sel,val

    #f=open('/home/niklasw/OpenFOAM/extend/TurboMachinery/README.svn')
    #print removeLines(f.read(),'=====','Policy')


