#!/usr/bin/python

from string import Template
import os

class htmlTemplate:
    def __init__(self, config):
        self.config = config
        templateFile= config.htmlTemplate
        self.OK = False
        self.content = ''
        try:
            with open(templateFile,'r') as fp:
                self.template = Template(fp.read())
                self.OK = True
        except:
            self.content = 'Template not found {0}'.format(templateFile)

    def addContent(self,c1='', c2='',c3='',c4='', curpage='index'):
        if self.OK:
            self.content = self.template.safe_substitute(content1=c1,
                                                         content2=c2,
                                                         content3=c3,
                                                         content4=c4,
                                                         currentpage=curpage)

    def __str__(self):
        return self.content

class htmlTable:

    def __init__(self, rowList):
        self.rows = rowList
        self.rowCounter = 0
        self.content = ''

    def newRow(self,cols, clst=('even','odd')):
        # Horisontally striping possilbe through CSS classes
        # even or odd
        cls = clst[self.rowCounter % len(clst)]
        r0 = '<tr class="{0}">'.format(cls)
        r1 = '</tr>'
        c = ' '.join(['<td>{0}</td>'.format(a) for a in cols])
        r = '{0} {1} {2}\n'.format(r0,c,r1)
        self.rowCounter += 1
        return r

    def new(self, cls='', head=[]):
        start = '<table class={0}>\n'.format(cls)
        end   = '\n</table>'
        header = self.newRow(head,clst=('head','head')) if head else ''
        rowList=[header]

        for row in self.rows:
            rowList.append(self.newRow(row))
        rows = '\n'.join(rowList)
        self.content = start+rows+end

class listLink:
    def __init__(self,name='**',href='#',cls=''):
        self.dictionary= {'name':name, 'href':href, 'class':cls}
        self.content = self.generate()

    def generate(self):
        line = '<li><a class="$class" href="$href">$name</a></li>'
        return Template(line).safe_substitute(self.dictionary)

    def __str__(self):
        return str(self.content)

class htmlList:
    def __init__(self,itemList=[], name='List'):
        self.items = itemList
        self.content=self.generate(head=name)

    def generate(self, head='List'):
        content = '<ul>\n'
        content+= '\t<li style="font-weight:bold;">{0}</li>\n'.format(head)
        content+= '\t<li>-----------</li>\n'
        for item in self.items:
            content+= '\t{0}\n'.format(item)
        content += '</ul>\n'
        return content

    def update(self, itemList, name='List'):
        self.items=itemList
        self.content = self.generate(head=name)

class dateSelector(htmlList):
    def __init__(self, name='dList', startYear=2013, endYear=2014, xdate='sdate',current='2013-01',curpage='index'):
        self.lines=[]
        for Y in range(startYear,endYear+1):
            dates = ['{0:04d}-{1:02d}'.format(Y, a) for a in range(1,13)]
            for date in dates:
                print date, 'curr date arg =', current
                cclass = 'current' if date == current else ''
                L = listLink(name=date,href='{2}?{0}={1}'.format(xdate,date,curpage),cls=cclass)
                self.lines.append(L)
        htmlList.__init__(self,self.lines, name)


def test():
    import sys,os
    from accountingTools import Configuration
    from os.path import join as pjoin

    configFile = pjoin(os.getcwd(),'config')

    C  = Configuration(configFile)

    A = []
    for i in range(5):
        r = []
        for j in range(4):
            r.append(j)
        A.append(r)

    table = htmlTable(A)
    doc = htmlTemplate(C)

    table.new(cls='mytable')

    doc.addContent(table.content)

    print doc

if __name__=='__main__':
    test()
