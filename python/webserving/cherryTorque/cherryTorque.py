#!/usr/bin/python

import cherrypy
from accountingTools import *
from os.path import join as pjoin
import cherryTemplates as CT
import utils

class Node(object):
    exposed = True

    def __call__(self):
        return "The node content"


class Root(object):

    def __init__(self, DB):
        self.node = Node()
        self.db = DB
        self.content = ''

    @cherrypy.expose
    def index(self, **kwargs):
        self.createPageContent(self.db.getProjectHours,'index',**kwargs)
        return self.content


    @cherrypy.expose
    def user(self, **kwargs):
        self.createPageContent(self.db.getUserHours,'user',**kwargs)
        return self.content


    def createPageContent(self,dbFunc, pageName, **kwargs):
        if kwargs.has_key('action'):
            if kwargs['action'] == 'update':
                self.db.update()
        if kwargs.has_key('date'):
            self.db.startTime = utils.date2epoch(kwargs['date'], '%Y-%m')
            print 'START TIME = ', self.db.startTime

        self.db.read()
        rows = dbFunc()
        document = CT.htmlTemplate(DB.conf)

        table = CT.htmlTable(rows)
        table.new(cls='mytable', head=['Project','Wall Time', 'CPU Time'])

        document.addContent(c1=table.content,c2='<p>Includes jobs started after {0}</p>'.format(epoch2date(self.db.startTime)),curpage=pageName)
        self.content = document.content

    @cherrypy.expose
    def download(self,filePath):
        """not implemented"""
        self.db.read()


class Download:
    """not implemented"""
    def index(self,filePath):
        return serve_file(filePath,"application/x-download", "attachment")
    index.exposed=True


if __name__ == '__main__':

    configFile = pjoin(os.getcwd(),'config')

    C  = Configuration(configFile)

    DB = DbManager(C)

    try:
        DB.update()
    except:
        Error('Could not update database!')

    cherrypy.config.update({'server.socket_port': C.serverPort,
                            'server.socket_host': '150.227.20.126',})
    root = Root(DB)
    #root.dl = Download()

    cherrypy.quickstart(root)


