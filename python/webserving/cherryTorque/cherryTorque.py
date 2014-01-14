#!/usr/bin/python

import os,cherrypy
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
        if kwargs.has_key('sdate'):
            self.db.startTime = utils.date2epoch(kwargs['sdate'], '%Y-%m')
            print 'START TIME = ', self.db.startTime
        if kwargs.has_key('edate'):
            self.db.endTime = utils.date2epoch(kwargs['edate'], '%Y-%m')
            print 'END TIME = ', self.db.endTime

        startDate = utils.epoch2date(self.db.startTime,'%Y-%m')
        endDate = utils.epoch2date(self.db.endTime,'%Y-%m')

        # Create date selector href lists
        DS1 = CT.dateSelector(name='Start date',
                              startYear=2013,
                              endYear=2014,
                              xdate='sdate',
                              current=startDate,
                              curpage=pageName)
        DS2 = CT.dateSelector(name='End date',
                              startYear=2013,
                              endYear=2014,
                              xdate='edate',
                              current=endDate,
                              curpage=pageName)

        self.db.read()
        rows = dbFunc()
        document = CT.htmlTemplate(DB.conf)

        table = CT.htmlTable(rows)
        table.new(cls='mytable', head=['Project','Wall Time', 'CPU Time'])

        informationParagraph = '''
        <p>Includes jobs started after {0}<br />
           and ended before {1} </p>'''.format(utils.epoch2date(self.db.startTime),
                                               utils.epoch2date(self.db.endTime))

        document.addContent(
                c1=table.content,
                c2=informationParagraph,
                c3=DS1.content,
                c4=DS2.content,
                curpage=pageName)

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
    from accountingTools import Configuration, DbManager

    configFile = pjoin(os.getcwd(),'config')

    C  = Configuration(configFile)

    DB = DbManager(C)

    #try:
    DB.update()
    #except:
    #    utils.Error('Could not update or sync database!')

    cherrypy.config.update({'server.socket_port': C.serverPort,
                            'server.socket_host': C.interfaceAddress,})
    root = Root(DB)
    #root.dl = Download()

    cherrypy.quickstart(root)


