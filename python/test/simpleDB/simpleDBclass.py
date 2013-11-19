#/usr/bin/env python2

import sys,os,string,re

class simpleDB:
    def __init__(self,dbRoot):
        self.root = dbRoot
        self.base = self.root+"/base"
        self.data = self.root+"/data"
        self.startTag = '<begin>'
        self.endTag = '<end>'
        self.itemTag = '<it>'
        self.sitemTag = '<sit>'
        self.ssitemTag = '<ssit>'
        self.sep1 = ':'

    def checkDBaccess(self):
        if not (os.access(self.root,os.F_OK) and \
                os.access(self.root,os.R_OK) and \
                os.access(self.root,os.W_OK) and \
                os.access(self.root,os.X_OK) and \
                os.access(self.base,os.F_OK) and \
                os.access(self.base,os.R_OK) and \
                os.access(self.base,os.W_OK) and \
                os.access(self.data,os.F_OK) and \
                os.access(self.data,os.R_OK) and \
                os.access(self.data,os.W_OK)):
            return 0
        else:
            return 1

    def checkDBaccsessOrDie(self):
        out = checkDBaccess()
        if not out:
            print 'Database files not accessilbe. Exiting'
            print 'PATH = '+self.data
            sys.exit(1)
        else:
            pass
        
    def createEmpty(self):
        out = self.checkDBaccess()
        if out:
            print 'Database files exists already. Exiting'
            print 'PATH = '+self.root
            sys.exit(1)
        else:
            os.mkdir(self.root)
            f = open(self.base,"w")
            f.write("###simpleDB base file")
            f.close
            f = open(self.data,"w")
            f.write("###simpleDB data file")
            f.close
        pass

    def readDB(self):
        f = open(self.data,'r')
        S = re.sub('\\n|\\r| ','',f.read())
        f.close()
        starti=S.index(self.startTag)+len(self.startTag)
        endi=S.index(self.endTag)
        S = S[starti:endi]
        return S

    def getKey(self, s):
        starti = s.index(self.sep1)+1
        endi = s.index(self.itemTag[0])
        key = s[starti:endi]
        return key

    def makeDict(self, S):
        L = S.split(self.itemTag)[1:]
        d = {}
        for item in L:
            d[self.getKey(item)]
            sL = item.split(self.sitemTag)
            for sitem in sL:
                print sitem

            #d{sL[0].split(':')}
            
            
        
    
    def edit():
        pass
    def append():
        pass
    def read():
        pass

def main():
    db1 = simpleDB("/home/wikstrom/develop/py/simpleDB/db1")
#    db1.createEmpty()
    S = db1.readDB()
    db1.makeDict(S)
main()
