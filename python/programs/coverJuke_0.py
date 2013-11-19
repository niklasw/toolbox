#!/usr/bin/python

import wx
from wx.lib.scrolledpanel import ScrolledPanel
import os,re,sys,string
from os.path import join as pjoin
from subprocess import Popen

class events:
    ID_FILE_TXT = 10
    ID_SUBMIT = 25
    ID_FILESELECT = 30
    ID_PLAY = 100
    ID_PAUSE = 101
    ID_STOP = 102
    ID_COVER_START = 200

def Warn(s):
    print "Warning: %s" % s

class Album:
    def __init__(self,path='',art=''):
        self.art = art
        self.path = path
        self.name = self.path.split(os.path.sep)[-1]
        self.artist = self.path.split(os.path.sep)[-2]
        self.tracks = None
        self.thumb = None
        self.getTracks()

    def getTracks(self):
        files = os.listdir(self.path)
        pat = re.compile('.*\.mp3|.*\.flac|.*\.ogg',re.I)
        self.tracks = []
        for (path,dirs,files) in os.walk(self.path):
            self.tracks += sorted(filter(pat.match,files))

    def createThumb(self,targetPath='',size=(300,300)):
        import Image,string
        # UGLY! Fix path stuff
        commonPrefix = os.path.commonprefix((targetPath,self.path))
        thumbFolder = pjoin(targetPath,string.lstrip(self.path,commonPrefix))
        if not os.path.isdir(thumbFolder):
            os.makedirs(thumbFolder)
        self.thumb = pjoin(thumbFolder,self.art)
        if not os.path.exists(self.thumb):
            img = None
            try:
                img = Image.open(pjoin(self.path,self.art))
            except:
                Warn('Cannot open image: %s' % self.art)
            img.resize(size).save(self.thumb)

class turnTable:
    def __init__(self):
        self.currentPid = None
        self.playList = []
        self.isPaused = False

    def signalPlayer(self,signal):
        p = Popen(['kill','-s',signal,str(self.currentPid)])
        p.wait()

    def play(self, playList):
        self.stop()
        p = Popen(['mplayer','-playlist', self.m3uFile])
        self.currentPid = p.pid
        self.isPaused = False

    def pause(self):
        if self.currentPid:
            if not self.isPaused:
                self.signalPlayer('STOP')
                self.isPaused = True
            else:
                self.signalPlayer('CONT')
                self.isPaused = False

    def stop(self):
        if self.currentPid:
            self.signalPlayer('KILL')
        self.currentPid = None
        self.isPaused = False


class DJ(dict):
    defaultPath = pjoin(os.getenv('HOME'),'Music')
    imagePattern = '.*cover.*\.jpg|.*front.*\.jpg|.*cover.*\.jpeg|.*front.*\.jpeg|.*cover.*\.png|.*front.*\.png'
    def __init__(self,path=defaultPath):
        dict.__init__(self)
        self.path = path
        self.albums = []
        self.nAlbums = len(self.albums)
        self.coverImages = [ a.art for a in self.albums ]
        self.coverSize = (200,200)
        self.currentAlbum = None
        self.thumbsFolder = pjoin(os.getenv('HOME'),'.albumPlayer')
        self.m3uFile = '/tmp/coverPlay.m3u'
        self.turnTable = turnTable()
        self.currentPid = None
        self.isPaused = False

    def update(self,*args,**kwargs):
        self.__init__(*args,**kwargs)

    def findAlbums(self,path=defaultPath):
        pat = re.compile(DJ.imagePattern,re.I)
        for (path,dirs,files) in os.walk(path):
            art = filter(pat.match,files)
            if len(art) > 0:
                self.albums.append(Album(path,art[0]))
        self.nAlbums = len(self.albums)

    def sortAlbums(self):
        from operator import attrgetter
        self.albums=sorted(self.albums,key=attrgetter('artist'))

    def createThumbs(self):
        for album in self.albums:
            album.createThumb(targetPath=self.thumbsFolder,size=self.coverSize)

    def createPlaylist(self):
        if self.currentAlbum:
            import string
            album = self.currentAlbum
            hdr = '#EXTM3U'
            lines = [hdr]
            for track in album.tracks:
                line=pjoin(album.path,track)
                lines.append(line)
            self.m3u = string.join(lines,'\n')
            m3uFPtr = open(self.m3uFile,'w')
            m3uFPtr.write(self.m3u)
            m3uFPtr.close()

    def signalPlayer(self,signal):
        p = Popen(['kill','-s',signal,str(self.currentPid)])
        p.wait()

    def play(self):
        self.createPlaylist()
        self.stop()
        p = Popen(['mplayer','-playlist', self.m3uFile])
        self.currentPid = p.pid
        self.isPaused = False

    def pause(self):
        if self.currentPid:
            if not self.isPaused:
                self.signalPlayer('STOP')
                self.isPaused = True
            else:
                self.signalPlayer('CONT')
                self.isPaused = False

    def stop(self):
        if self.currentPid:
            self.signalPlayer('KILL')
        self.currentPid = None
        self.isPaused = False

    def cleanup(self):
        self.stop()

class botButtons(wx.Panel):
    def __init__(self,parent,*args,**kwargs):
        wx.Panel.__init__(self,parent,*args,**kwargs)

        global dj

        sizer = wx.GridSizer(rows=1,cols=4)

        quitButton = wx.Button(self, id=wx.ID_EXIT, label='Quit')
        self.Bind(wx.EVT_BUTTON, self.OnExit, id=wx.ID_EXIT)

        playButton = wx.Button(self, id=events.ID_PLAY, label='Play')
        self.Bind(wx.EVT_BUTTON,self.OnPlay,id=events.ID_PLAY)

        pauseButton = wx.Button(self, id=events.ID_PAUSE, label='Pause/Resume')
        self.Bind(wx.EVT_BUTTON,self.OnPause,id=events.ID_PAUSE)

        stopButton = wx.Button(self, id=events.ID_STOP, label='Stop')
        self.Bind(wx.EVT_BUTTON,self.OnStop,id=events.ID_STOP)

        sizer.Add(playButton, flag=wx.ALIGN_LEFT)
        sizer.Add(pauseButton, flag=wx.ALIGN_LEFT)
        sizer.Add(stopButton, flag=wx.ALIGN_LEFT)
        sizer.Add(quitButton, flag=wx.ALIGN_RIGHT)

        self.SetSizer(sizer)
        self.Fit()

    def OnPlay(self,e):
        dj.play()

    def OnPause(self,e):
        dj.pause()

    def OnStop(self,e):
        dj.stop()

    def OnExit(self,e):
        self.Parent.Destroy()


class albumCoverPanel(ScrolledPanel):
    def __init__(self,*args,**kwargs):
        ScrolledPanel.__init__(self,*args,**kwargs)

        global dj

        nCoverCols = 2
        nCoverRows = dj.nAlbums/nCoverCols+1
        self.sizer = wx.GridSizer(rows=nCoverRows,cols=nCoverCols,vgap=5,hgap=5)

        self.SetMinSize((nCoverCols*dj.coverSize[0]+55,dj.coverSize[1]))

        for i, album in enumerate(dj.albums):
            ID = events.ID_COVER_START+i
            button = wx.BitmapButton(self,id=ID,bitmap=wx.Bitmap(album.thumb),size=dj.coverSize,name=str(i))
            button.Bind(wx.EVT_BUTTON,self.OnPressCover,id=button.GetId())
            button.SetToolTipString(string.join([album.artist,album.name],'\n'))
            self.sizer.Add(button,flag=wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling(scroll_y=True, scroll_x=False)

    def OnPressCover(self,e):
        b = e.GetEventObject()
        albumIndex = b.GetId()- events.ID_COVER_START
        if dj.albums[albumIndex] == dj.currentAlbum:
            dj.play()
        else:
            dj.currentAlbum = dj.albums[albumIndex]
            self.Parent.albumPanel.OnPressCover()

class albumInfoPanel(ScrolledPanel):
    def __init__(self,*args,**kwargs):
        ScrolledPanel.__init__(self,*args,**kwargs)

        global dj

        self.sizer = wx.FlexGridSizer(rows=100,cols=2)

        box = wx.StaticBox(self,label='Album tracks') #,size=(400,500))
        boxSizer = wx.StaticBoxSizer(box,orient=wx.VERTICAL)

        self.clear()

        boxSizer.Add(self.sizer, flag=wx.EXPAND|wx.ALL, border=5)
        boxSizer.Fit(self)

        self.SetSizerAndFit(boxSizer)
        self.SetAutoLayout(1)

    def OnPressCover(self):
        self.clear()
        self.sizer.Add(wx.StaticText( self, label = dj.currentAlbum.name ))
        self.sizer.Add(wx.StaticText( self, label = dj.currentAlbum.artist ))
        self.sizer.Add(wx.StaticLine( self, size=(180,20), name = 'Artist' ))
        self.sizer.Add(wx.StaticLine( self, size=(180,20) , name = 'Album' ))
        for mediaFile in dj.currentAlbum.tracks:
            track,ext = os.path.splitext( os.path.basename(mediaFile) )
            ext = ext.lstrip('.')
            self.sizer.Add(wx.StaticText(self,label=track))
            self.sizer.Add(wx.StaticText(self,label=ext),flag=wx.ALIGN_LEFT)
            self.Update()
            self.SetupScrolling(scroll_y=True, scroll_x=True)

    def clear(self):
        self.sizer.Clear(deleteWindows=True)
        #self.sizer.Add(wx.StaticText(self,label='Type    '))
        #self.sizer.Add(wx.StaticText(self,label='Name'),flag=wx.ALIGN_LEFT)
        self.Update()


class window0(wx.Frame):
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)

        global dj

        windowWidth,windowHeight = self.GetSize()
        coverWidth,coverHeight = dj.coverSize
        self.sizer = wx.FlexGridSizer(rows=1,cols=2)

        self.leftBox = wx.StaticBox(self,label='Select Album (%d)' % dj.nAlbums)
        self.leftBoxSizer = wx.StaticBoxSizer(self.leftBox)

        self.rightBoxSizer = wx.FlexGridSizer(rows=2,cols=1)

        self.albumPanel = albumInfoPanel(self)
        self.albumPanel.SetMinSize((1.5*coverWidth,3*coverHeight))

        self.coverPanel = albumCoverPanel(self)

        self.buttonsPanel = botButtons(self)

        self.leftBoxSizer.Add(self.coverPanel,flag=wx.EXPAND)

        self.rightBoxSizer.Add(self.albumPanel,flag=wx.EXPAND)
        self.rightBoxSizer.Add(self.buttonsPanel,flag=wx.EXPAND)

        self.sizer.Add(self.leftBoxSizer,flag=wx.EXPAND|wx.ALL,border=10)
        self.sizer.Add(self.rightBoxSizer,flag=wx.EXPAND|wx.ALL, border=10) 

        self.SetSizerAndFit(self.sizer)
        self.Center()

if __name__=='__main__':
    dj = DJ()
    dj.findAlbums()
    dj.sortAlbums()
    dj.createThumbs()

    app = wx.App()
    mainFrame = window0(None,title='player')
    mainFrame.Show()
    app.MainLoop()

    dj.cleanup()

