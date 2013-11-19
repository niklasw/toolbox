#!/usr/bin/python

import sys,os,re

class project(dict):

    def __init__(self,root='.',dirName='',number='',name=''):
        self.pattern = re.compile('^([\w]{4})_(\w*)')
        self.check=False
        self.adminFile='.projectAdmin'
        self.root = root
        dict.__init__(self,
                     {'name':name,
                      'number':number,
                      'dirName':dirName})
        self.initFromDir()

    def __str__(self):
        return '%30s%30s%6s' % (self['dirName'], self['name'], self['number'])

    def initFromDir(self):
        if self['dirName']:
            match = self.pattern.match(self['dirName'])
            if match:
                (self['number'],self['name']) = match.groups()
                self.check=True


class projectList(list):

    def __init__(self,projectsDataDir,pList=[]):
        self.projectsDir = projectsDataDir
        self.projects = pList
        self.nProjects = len(self.projects)
        list.__init__(self,self.projects)

    def Print(self):
        for item in self:
            print item

    def getProjectsFromProjectsDir(self):
        for d in os.listdir(self.projectsDir):
            curProj = project(root=self.projectsDir, dirName=d)
            if curProj.check:
                self.append(curProj)

def test():

    projDir = '/fsdsth/proj1/uppdrag'
    pList = projectList(projDir)
    pList.getProjectsFromProjectsDir()

    pList.Print()

if __name__=="__main__":
    test()
