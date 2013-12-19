#!/usr/bin/python


# A note on accounting records:
# ctime   time job was created
# etime   time job was queued
# qtime   time job became eligible to run
# start   time job started to run

# D   delete  job has been deleted
# E   exit    job has exited (either successfully or unsuccessfully)
# Q   queue   job has been submitted/queued
# S   start   an attempt to start the job has been made (if the job fails to properly start, it may have multiple job start records)

import os,sys,re
from utils import *

debugSql = False

class Configuration:
    # Config sections
    main = 'Main'
    site = 'Site'
    db = 'Db'

    def __init__(self,confFile):
        import ConfigParser as Conf
        config = Conf.ConfigParser()
        config.read(confFile)

        self.logsPath = config.get(self.db, 'path')
        self.database = config.get(self.db,'database')
        self.logFileGlob = config.get(self.db, 'glob')
        self.serverLogsPath = config.get(self.db,'serverLogsPath')

        self.serverPort = int(config.get(self.site,'port'))
        self.htmlTemplate = config.get(self.site,'htmlTemplate')


class jobDb:
    tableDef = [
                   ('user','TEXT'),
                   ('group','TEXT'),
                   ('jobname','TEXT'),
                   ('status','TEXT'),
                   ('pid','TEXT'),
                   ('queue','TEXT'),
                   ('ctime','INT'),
                   ('qtime','INT'),
                   ('etime','INT'),
                   ('start','INT'),
                   ('owner','TEXT'),
                   ('exec_host','TEXT'),
                   ('Resource_List_other','TEXT'),
                   ('Resource_List_nodes','INT'),
                   ('Resource_List_walltime','INT'),
                   ('resources_used_walltime','INT'),
                   ('resources_used_cputime','INT'),
                   ('session','INT'),
                   ('end','INT'),
                   ('resources_used_cput','TEXT'),
                   ('resources_used_vmem','TEXT')
               ]
    tableName = 'Jobs'

    def __init__(self, dbFileName='torqueLog'):
        self.tableOk = True # Born without sin
        self.dbFileName = dbFileName
        self.conn = None

    def read(self):
        import sqlite3 as sql
        if os.path.exists(self.dbFileName):
            self.newDb = False
            self.conn = sql.connect(self.dbFileName)
        else:
            Error('Cannot read from db {0}'.format(self.dbFileName))

    def new(self):
        import sqlite3 as sql
        self.conn = sql.connect(self.dbFileName)
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS Jobs")
            tableCont = ', '.join( [ 'I'+k+' '+v for k,v in self.tableDef ] )
            createCmd = 'CREATE TABLE %s( Id INTEGER PRIMARY KEY, %s)' % (self.tableName,tableCont)
            cursor.execute(createCmd)

    def checkTables(self):
        # Check if existing table contains at least definitions in tableDef.
        Error('NOT IMPLEMENTED')
        result = self.sqlQuery('PRAGMA table_info(%s)' % self.tableName)
        dbColumns = [ c.split('|') for c in result ]
        for item in self.tableDef:
            if item in dbColumns:
                print item

        return dbColumns

    def addJob(self,job):
        cursor = self.conn.cursor()
        values=[]
        for key,val in self.tableDef:
            if val == 'TEXT':
                values.append("%s" % (job[key],))
            elif val == 'INT':
                values.append(job[key])

        sql = "INSERT INTO Jobs VALUES(NULL%s)" % (len(values)*', ?')
        cursor.execute(sql, (values))


    def write(self):
        data = '\n'.join(self.conn.iterdump())
        self.conn.commit()

    #@timeit
    def sqlQuery(self,query):
        with self.conn:
            cursor=self.conn.cursor()
            if debugSql: print query
            cursor.execute(query)
            return cursor.fetchall()

class DbManager(jobDb):

    def __init__(self, conf):
        self.conf = conf
        jobDb.__init__(self,conf.database)
        self.startTime = 0


    def syncTorqueLogs(self):
        from subprocess import Popen, PIPE
        source = self.conf.serverLogsPath+'/'+self.conf.logFileGlob
        target = self.conf.logsPath+'/'
        cmd = ['/usr/bin/rsync',source,target]
        p = Popen(cmd, stdout=PIPE)
        out,err = p.communicate()
        if err:
            Warn('Could not sync logs from torque server')
        else:
            Info('Sync from torque server successful')



    def update(self):
        import glob
        from os.path import join as pjoin
        self.syncTorqueLogs()
        torqueLogs = glob.glob(pjoin(self.conf.logsPath,self.conf.logFileGlob))
        parser = torqueParser(torqueLogs)
        parser.parse()
        self.new()
        for i, item in enumerate(parser.jobList):
            self.addJob(item)
        self.write()

    def getUniqeList(self, column):
        result = self.sqlQuery('SELECT DISTINCT {0} FROM {1}'.format(column,self.tableName))
        return sorted([item[0] for item in result])

    def getProjectList(self):
        return self.getUniqeList('IResource_List_other')

    def getUserList(self):
        return self.getUniqeList('iuser')

    def getCPUHours(self, resource, userList):
        rows = []
        totalWallTime = 0
        totalCPUTime = 0
        for user in userList:
            if user == 'NOVALUE':
                continue
            cpuTime = 0
            wallTime = 0
            result = self.sqlQuery("""
            SELECT IResource_List_nodes, iresources_used_walltime FROM Jobs Where istatus = 'E'
            and {0} = '{1}' and istart >= {2}
            """.format(resource, user, self.startTime)) # List of tuples [(n,secs), (n,secs)...]
            if result:
                coreCounts= result[0]

                wallTime = sum([a[1] for a in result])
                cpuTime = sum([a[0]*a[1] for a in result])

                totalWallTime += wallTime
                totalCPUTime += cpuTime

            rows.append((str(user), s2hms(wallTime),s2hms(cpuTime)))

        rows.append(('----','----','----'))
        rows.append(('TOTAL', s2hms(totalWallTime),s2hms(totalCPUTime)))
        return rows

    def getProjectHours(self):
        return self.getCPUHours('IResource_List_other',self.getProjectList())

    def getUserHours(self):
        return self.getCPUHours('iuser',self.getUserList())

class Job(dict):
    mandatoryKeys = [ a[0] for a in jobDb.tableDef ]
    accountKey = 'Resource_List_other'
    wallTimeKey= 'resources_used_walltime'
    nodeCountKey = 'Resource_List_nodes'

    def __init__(self, line, d={}):
        dict.__init__(self,d)
        self.defaultDict()
        self.parseLine(line)
        self.OK = True #self.assertAllKeys()

    def gatherInfo(self,s):
        # Hack up semi-colon separated second field
        # and assign these sub-fields directly. "user"
        # is however a "key=value" pair, and is returned
        # for later treatement in parseLine()
        sSplit = s.split(';')
        try:
            self['clockStr'] = sSplit[0]
            self['status'] = sSplit[1]
            self['pid']= sSplit[2]
            return sSplit[-1]
        except:
            Warn('Could not gather info from string %s'%s)
            return 'user=NOTFOUND'

    def parseLine(self,l):
        # Most fields of a line are key=value pairs, but the first and
        # second fields need special treatment. Hence, popping these
        # and gather their information separately.
        splitLine = l.split()
        #self.clear()
        self['dateStr'] = splitLine.pop(0)
        infoStr = splitLine.pop(0)
        user = self.gatherInfo(infoStr)
        splitLine.append(user)

        for item in splitLine:
            keyVal = item.split('=',1)
            key = re.sub('\.','_',keyVal[0]) # To fit SQL. No dots in sql keys.
            if re.search(self.wallTimeKey,key):    # Special treatment of time string
                keyVal[1] = hms2s(keyVal[1])
            if re.search(self.nodeCountKey,key):
                keyVal[1] = coreCount(keyVal[1])
            self[key] = keyVal[1]

    def defaultDict(self):
        # Fill dictionary with empty values. Needed for sqlite.
        self['dateStr'] = ''
        self['clockStr'] = ''
        self['status'] = ''
        self['pid'] = ''
        for key,typ in jobDb.tableDef:
            self[key] = -1 if typ == 'INT' else 'NOVALUE'

    def assertAllKeys(self):
        OK = True
        for key in self.mandatoryKeys:
            if not self.has_key(key):
                #Warn('Missing key %s in %s' % (key,self['pid']))
                OK = False
                break
        return OK

    def duration(self):
        pass


class torqueParser(dict):
    def __init__(self, fileList = []):
        dict.__init__(self)
        self.jobList = []
        self.files = fileList

    def parseFile(self,fp):
        jobList = []
        for line in fp:
            job = Job(line)
            if job.OK:
                jobList.append( job )
        return jobList

    @timeit
    def parse(self):
        for f in self.files:
            #try:
                with open(f,'r') as fp:
                    self.jobList+=self.parseFile(fp)
            #except:
            #    Warn('Could not open %s' % f)



def test():
    fileNames = list(sys.argv[2:])
    dbFile = sys.argv[1]

    jdb = jobDb(dbFile)

    if os.path.exists(dbFile):
        jdb.read()
    else:
        parser = torqueParser(fileNames)
        parser.parse()

        jdb.new()
        for i, item in enumerate(parser.jobList):
            jdb.addJob(item)
        jdb.write()

    result = jdb.sqlQuery("SELECT ipid FROM Jobs") #  WHERE iuser='fureby' and istatus='E' ")
    print len(result)
    result = set(result)
    print len(result)

    projectList = jdb.sqlQuery('select distinct IResource_List_other from jobs')

    for project in projectList:
        wallSecs = jdb.sqlQuery("SELECT SUM(iresources_used_walltime) FROM Jobs WHERE istatus = 'E' and IResource_List_other = '%s'" % project)
        if project[0] != 'NOVALUE':
            print project, s2hms(wallSecs[0][0])


if __name__=='__main__':
    test()


