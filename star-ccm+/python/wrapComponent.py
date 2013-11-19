#!/usr/bin/env python

import os,sys,re,tarfile

prog=os.path.basename(sys.argv[0])
location=os.path.dirname(sys.argv[0])

class color:
    HEAD = '\033[95m'
    OK= '\033[92m'
    WARN= '\033[95m'
    ERR = '\033[95m'
    END = '\033[0m'

class Interactor:

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

    def fileSelector(self,prompt='Select input file',default='',path='',suffix='*',folder=False):
        import glob
        globbed = glob.glob(os.path.join(path,'*'+suffix))
        if not globbed: self.error('No matching input files found (%s)'%suffix)
        if not os.path.isfile(default): default=globbed[0]

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

class values:
    #Default values
    baseSize=10.0
    minSize=20
    wScale=50
    inputFile=''
    outputFile=''
    templateKeys={}

    # File names
    templateArchive=os.path.join(location,"wrapComponent_templates.tar")
    wrapTemplate="wrapComponent_ccmWrapper.template"
    saveTemplate="wrapComponent_ccmSaver.template"
    prepTemplate="wrapComponent_powerprep.template"
    simTemplate="wrapComponent.sim"
    config="lastWrap.py"

    # File names temporary files
    wrapBatch='wrapper.java'
    saveBatch='saver.java'
    prepBatch='prep.py'
    wrapLog='wrapper.log'
    starSimDefault='wrapComponent.sim'

    # Executables
    starexe='/share/apps/cd-adapco/RHEL5/v6.06.011/STAR-CCM+6.06.011/star/bin/starccm+'
    prepexe='powerflow -exe powerprep'
    starGuiMode='-batch'

    starbatOption='-batch'

    def __init__(self):
        for file in [os.path.join(location,self.templateArchive),self.starexe]:
            if not os.path.isfile(file):
                print ('Mandatory file is missing: %s' % file)
                sys.exit(1)
        pass

    def store(self,f='lastWrap.py'):
        fh=open(f,'w')
        fh.write('baseSize = %s\n'% self.baseSize)
        fh.write('minSize = %s\n'% self.minSize)
        fh.write('wScale = %s\n'% self.wScale)
        fh.write('inputFile = "%s"\n'% self.inputFile)
        fh.close()

    def update(self):
        if self.inputFile:
            self.outputFile=os.path.splitext(self.inputFile)[0]+'_CCMWRAP.stl'

        self.templateKeys={'__INPUT_FILE__':self.inputFile,
                           '__BASESIZE__':str(self.baseSize),
                           '__RELATIVE_MINSIZE__':str(self.minSize),
                           '__OUTPUT_FILE__':self.outputFile,
                           '__WRAPPER_SCALE__':str(self.wScale)}


def Fatal(s,exitStatus=1):
    print color.ERR+s+color.END
    sys.exit(exitStatus)

def Warn(s):
    print color.WARN+s+color.END

def Info(s):
    print color.OK+s+color.END

def fetchTemplate(name,db):
    t=tarfile.open(db.templateArchive)
    return t.extractfile(name).read()

def buildFromTemplate(name,db):
    s=fetchTemplate(name,db)
    for key,value in db.templateKeys.iteritems():
        s=re.sub(key,value,s)
    return s

def listAvailableFiles(suff='stl'):
    import glob
    return glob.glob('*.'+suff)

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
    Warn("NOTE StarCCM+ imports surface file in meters!!")
    Warn("\nNOTE If you choose to launch StarCCM+ in gui mode,\nyou MUST use the saver.java macro to export the wrapped geometry!")
    db=values()

    # Read values from last session if exists
    try:
        import lastWrap
        Info('Importing settings from last run.')
    except:
        lastWrap=db

    stlFiles = listAvailableFiles()

    interactor = Interactor()

    # Read input from terminal
    db.inputFile = interactor.fileSelector(prompt='Input file',default=lastWrap.inputFile,suffix='.stl')
    db.baseSize  = interactor.get(prompt='Base size',default=lastWrap.baseSize,test=float)
    db.minSize   = interactor.get(prompt='Min relative surface size',default=lastWrap.minSize,test=int)
    db.wScale    = interactor.get(prompt='Wrapper scale factor',default=lastWrap.wScale,test=int)
    gui          = interactor.get(prompt='Launch starccm+ GUI?', default='n',test=str)
    if not gui == 'n':
        db.starGuiMode = '-macro'
    else:
        db.starSimDefault = ''
    db.update()
    db.store()

    s=buildFromTemplate(db.wrapTemplate,db)
    if db.starGuiMode == '-macro':
        s = removeLines(s,'JAVA_START_GENERATE_MESH','JAVA_END_GENERATE_MESH')
    open(db.wrapBatch,'w').write(s)
    if db.starGuiMode == '-macro':
        s=buildFromTemplate(db.saveTemplate,db)
        open(db.saveBatch,'w').write(s)
    s=buildFromTemplate(db.prepTemplate,db)
    open(db.prepBatch,'w').write(s)
    if db.starSimDefault:
        s=fetchTemplate(db.simTemplate,db)
        open(db.starSimDefault,'w').write(s)

    import subprocess
    import string
    # Launch starccm+
    starcmd = string.join([db.starexe, db.starGuiMode, db.wrapBatch, db.starSimDefault])
    Info(starcmd)
    ccmretval = subprocess.call(starcmd, stdout=file(db.wrapLog,'w'), stderr=file('wrapper.err','w'), shell=True)
    prepretval = 0

    if ccmretval == 0:
        Info("Successfully wrapped.\nLaunching powerprep for you.")
        prepcmd = string.join([db.prepexe, '-script', db.prepBatch])
        prepretval = subprocess.call(prepcmd,shell=True)
    else:
        Fatal("Wrapping failed!")

    if ccmretval == 0 and prepretval == 0:
        for file in ['lastWrap.pyc',db.wrapBatch,db.prepBatch,db.saveBatch,db.starSimDefault]:
            if os.path.isfile(file): os.remove(file)





