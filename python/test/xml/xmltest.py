#!/usr/bin/python

import sys
import xml.dom.minidom as DOM
from xml.dom.minidom import Node,Document
from xml.dom.ext import PrettyPrint
from xml import xpath

class ansysCase:
    cName='case'
    optName='options'
    mandatoryCaseAtts=[('user','guest'),('id','')]
    mandatoryCaseOpts=[('dir','/tmp'),('j','file')]

    def __init__(self,doc):
        self.node=doc.createElement(ansysCase.cName)
        options=doc.createElement(ansysCase.optName)
        self.node.appendChild(options)
        self.setDefault()

    def node(self):
        return self.node

    def setDefault(self):
        self.setAtts()
        self.setOptions()

    def setAtts(self,atts=[]):
        import time
        for att in ansysCase.mandatoryCaseAtts:
            self.node.setAttribute(att[0],att[1])
            self.node.setAttribute('time',str(time.time()))
        for att in atts:
            self.node.setAttribute(att[0],att[1])

    def parseOptions(self,flagstring):
        alist=flagstring.split()
        def getnext(alist):
            try:
                astring=alist.pop()
                if astring[0] == '-':
                    print 'parseOptions: Syntax error in argument list near: '+astring
                    sys.exit(14)
                return astring
            except:
                print 'parseOptions: Exception error during argument list parsing'
                sys.exit(15)
        hash={}
        alist.reverse()
        while len(alist):
            opt=alist.pop()
            if opt=='-m':
                hash['m']=getnext(alist)
            elif opt=='-dir':
                hash['dir']=getnext(alist)
            elif opt=='-db':
                hash['db']=getnext(alist)
            elif opt=='-p':
                hash['p']=getnext(alist)
            elif opt=='-i':
                hash['i']=getnext(alist)
            elif opt=='-o':
                hash['o']=getnext(alist)
            elif opt=='-j':
                hash['j']=getnext(alist)
            elif opt=='-b':
                pass
            else:
                print 'parseOptions: WARNING, unrecognised option '+opt+' encountered.'
        if not hash.has_key('dir'):
            print 'parseOptions(): option -dir was not found in the submission.'
            sys.exit(16)

        return hash


    def setOptions(self,opts=[]):
        optN=xpath.Evaluate('options',self.node)[0]
        for opt in ansysCase.mandatoryCaseOpts:
            optN.setAttribute(opt[0],opt[1])
        for opt in opts:
            optN.setAttribute(opt[0],opt[1])

class queue:
    lockSuffix='.lock'
    def __init__(self,db,dbstr=''):
        self.db=db
        self.lock=lockFile(self.db+queue.lockSuffix)
        try:
            if dbstr ==  '':
                self.doc=DOM.parse(self.db)
            else:
                self.doc=DOM.parseString(dbstr)
        except:
            print 'Could not parse DOM from file '+self.db
            sys.exit(1)
        self.root=self.doc.firstChild
        self.caseList=self.root.getElementsByTagName(ansysCase.cName)
        self.allCases=self.caseList

    def reduceCaseListByAttributes(self,atts):
        # where atts is a tuple list (att,value)
        while atts:
            att=atts.pop()
            for i,case in enumerate(self.caseList):
                if not case.getAttribute(att[0])==att[1]:
                    self.caseList.pop(i)

    def reset(self):
        del self.lock
        self.__init__(self.db)

    def purgeCaseList(self):
        for case in self.caseList:
            self.root.removeChild(case)

    def save(self):
        PrettyPrint(self.doc,open(self.db,'w'))
        del self.lock

    def appendCase(self,caseN):
        self.caseList.append(caseN)
        self.root.appendChild(caseN)

    def appendDefaultCase(self):
        self.appendCase(ansysCase(self.doc).node)

class subQueue(queue):
    def __init__(self,db):
        self.subdb=db
        queue.__init__(self,db,self.wrap())
        self.paramsList=[]
        for caseN in self.allCases:
            self.paramsList.append(caseN.firstChild.nodeValue)

    def wrap(self):
        header='<?xml version="1.0" encoding="iso-8859-1"?>'
        return header+'\n<submitdb>\n'+open(self.subdb,'r').read()+'\n</submitdb>\n'


class lockFile:
    def __init__(self,file):
        self.file=file
        self.lock()
    def __del__(self):
        print 'Unlock and clear lock.'
        self.unlock()

    def lock(self):
        import os,time
        while os.path.isfile(self.file):
            print 'waiting for',self.file,'to disappear'
            time.sleep(1)
        else:
            fh=open(self.file,'w')
            fh.close()

    def unlock(self):
        import os
        if os.path.isfile(self.file):
            if not os.access(self.file,os.W_OK):
                print 'lock: no write permission on lock.'
                sys.exit(1)
            else:
                os.remove(self.file)

def testQ1(db,atts):
    Q = queue(db)
    Q.reduceCaseListByAttributes(atts)
    Q.purgeCaseList()
    Q.save()
    PrettyPrint(Q.doc)

def testQ2(db):
    Q = queue(db)
    print 'Q2'
    Q.appendDefaultCase()
    PrettyPrint(Q.doc)
    Q.save()

if __name__=='__main__':
    import thread,time
    db='/home/nikwik/usr/local/var/runsys/db.xml'
    atts=[('user','a403918'),('status','finished')]
    atts2=[('pid','7196'),('status','finished')]

    dropQ=subQueue('/home/nikwik/runsys/var/case.xml')
    for c in dropQ.allCases:
        print c

    testQ1(db,atts)
    time.sleep(.1)
    thread.start_new_thread(testQ2,(db,))
    thread.start_new_thread(testQ2,(db,))

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print 'stop monitoring...'
            break
        except Exception, err:
            print err       

