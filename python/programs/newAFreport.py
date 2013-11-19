#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys,shutil

prog=os.path.basename(sys.argv[0])

def usage(exit=True):
    print "\nUsage:\n",prog," <directory>"
    print """
    This python script needs a file
    containing config files for the report
    generation. Normaly $HOME/.aftex/config

    Some or several of these criteria is not met.

    """
    if exit:
        print "Exiting.\n"
        sys.exit(1)

def copyFile(f0,f1):
    if os.path.isfile(f0):
        if os.path.isfile(f1):
            ow = interactor('File exists '+f1+'. Overwrite? [y/n]')
            if ow!='y':
                return False
        shutil.copyfile(f0,f1)
        return True
    else:
        print 'No such file',f0
        return False

def makeDir(d0):
    if os.path.isdir(d0):
        print 'Report directory exists.'
        ow = interactor('Remove '+d0+' and create new? [y/n]')
        if ow != 'y':
            sys.exit(2)
        else:
            shutil.rmtree(d0)
    try:
        os.mkdir(d0) 
    except:
        print 'could not create directory',d0
        sys.exit(3)

def interactor(astring):
    print astring
    return sys.stdin.readline().strip()


def lookup(h,tag):
    h.seek(0)
    ret=''
    for line in h.readlines():
        if line.split('=')[0].strip() == tag:
            ret = line.split('=')[1].strip()
    if ret == '':
        print "In lookup.",tag,"not found."
        return None
    else:
        return ret

def chkConfig(pathto):
    out=True
    if not os.path.isfile(pathto):
        out=false
    return out

def substKeyword(afile,keywords):
    import re
    print afile
    fh=open(afile,'r')
    lines=fh.read()
    fh.close()
    for key in keywords:
        pat=re.compile(key)
        print key,keywords[key]
        lines=re.sub(pat,keywords[key],lines)
    fh=open(afile,'w')
    fh.write(lines)

def createDirName(astring):
    import re
    pat=re.compile(r'\s+')
    return re.sub(pat,'_',astring)

config=os.path.join(os.getenv('HOME'),'.aftex/config')
pwd=os.getcwd()

if not chkConfig(config):
    sys.exit(1)
 
docname='Test'
lang='en'
auth=u'Niklas Wikstrom'
ref='NW'

if sys.argv[1] != "test":
    docname=interactor('Report name: ')
    lang=interactor('Language [sv/en]:')
    auth=interactor('Author name: ')
    ref=interactor('Our reference: ')

templateKeyWords={'AF-template-AUTHORNAME':auth,
        'AF-template-REFERENCE':ref,
        'AF-template-REPORTNO':'XXX',
        'AF-template-TITLE':docname}

confh=open(config,'r')
tplpath      = lookup(confh,'root')
preamble     = lookup(confh,'preamble')
common_tex   = lookup(confh,'common_tex').split(',')
files_tex    = lookup(confh,'files_tex').split(',')
common_files = lookup(confh,'common').split(',')
main_file    = lookup(confh,'file_main').split(',')[0]
suffix_tex   = '.'+lookup(confh,'suffix_tex').split(',')[0]

lang_tag='-'+lang
if lang!='sv' and lang!='en':
    print 'language ',lang,'is not supported. try en or sv.'
    usage()

report_dir=os.path.join(pwd,createDirName(docname))
includes_dir=os.path.join(report_dir,'includes')
makeDir(report_dir)
makeDir(includes_dir)

for f in common_files:
    copyFile(os.path.join(tplpath,f),os.path.join(includes_dir,f) )

for f in common_tex:
    f2=preamble+f+suffix_tex
    print "copyFile",f2
    copyFile(os.path.join(tplpath,f2),os.path.join(includes_dir,f2) )

for f in files_tex:
    f2=preamble+f+lang_tag+suffix_tex
    print "copyFile",f2
    copyFile(os.path.join(tplpath,f2),os.path.join(includes_dir,f2) )
    substKeyword(os.path.join(includes_dir,f2), templateKeyWords)

f2 = preamble+main_file+lang_tag+suffix_tex
copyFile(os.path.join(tplpath,f2),os.path.join(report_dir,f2) )

print "\nEnd.\n"

