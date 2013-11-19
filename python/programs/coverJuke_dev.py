#!/usr/bin/python

import wx
from wx.lib.scrolledpanel import ScrolledPanel
import os,re,sys,Image,string,time
from os.path import join as pjoin
from subprocess import Popen

from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis

def Warn(s):
    print "Warning: %s" % s


def fakeAlbumCover(artist,name,size,path):
    drawString = """fill olive  circle 250,130 310,30 \
                   fill maroon circle 55,75 15,80 \
                   font Helvetica  font-size 42 \
                   fill darkgrey  stroke grey  stroke-width 2 \
                   translate 10,210 rotate -0 text 0,0 '%s'""" % string.join([artist,name],'\n')
    cmd=['convert']
    cmd+=['-size',string.join(map(str,size),'x'),'xc:black']
    cmd+=['-draw',drawString]
    cmd+=[pjoin(path,'cover.png')]
    print cmd
    Popen(cmd)

# - - - - - - - - - - - - - - - - - - - - -

class events:
    ID_FILE_TXT = 10
    ID_SUBMIT = 25
    ID_FILESELECT = 30
    ID_PLAY = 100
    ID_PAUSE = 101
    ID_STOP = 102
    ID_NEXT = 103
    ID_PREV = 104
    ID_COVER_START = 200

# - - - - - - - - - - - - - - - - - - - - -

class metaReader(dict):
    knownExtensions = ['OGG','FLAC','MP3']
    albumTag = 'album'
    artistTag = 'artist'
    titleTag = 'title'
    numberTag = 'tracknumber'
    def __init__(self,path='',fname=''):
        dict.__init__(self)
        self.fileName = fname
        self.file=pjoin(path,fname)
        if self.fileName: self.getFiletypeByExtension()
        self.reader = None
        self.isAudio = False

    def getFiletypeByExtension(self):
        EXT = (os.path.splitext(self.fileName)[-1]).upper().strip('.')
        if EXT in self.knownExtensions:
            self.fileType = EXT
            self.isAudio = True
        else:
            self.fileType = None
            self.isAudio = False
        return self.isAudio

    def getFiletype(self):
        return self.getFiletypeByExtension()

    def setReader(self):
        if self.fileType == 'FLAC' : self.reader = FLAC(self.file)
        elif self.fileType == 'MP3': self.reader = EasyID3(self.file)
        elif self.fileType == 'OGG': self.reader = None

    def l2s(self,item,sep=''):
        return string.join(item,sep)

    def getAlbum(self,default='Unknown Album'):
        try:
            out = self.l2s(self.reader[self.albumTag])
        except:
            out = default
        return out

    def getArtist(self, default='Unknown Artist'):
        try:
            out = self.l2s(self.reader[self.artistTag])
        except:
            out = default
        return out

    def getTitle(self, default='Unknown Track Title'):
        try:
            out = self.l2s(self.reader[self.titleTag])
        except:
            out = default
        return out

    def getNumber(self, default=0):
        try:
            out = int( self.l2s(self.reader[self.numberTag]) )
        except:
            out = default
        return out

# - - - - - - - - - - - - - - - - - - - - -

def collectAlbums(root):
    albums = {}
    for (path,dirs,files) in os.walk(root):
        for f in files:
            m = metaReader(path,f)
            trck=None
            if m.fileType:
                try:
                    m.setReader()
                    album = m.getAlbum()
                    trck = track(m.getTitle(),m.getNumber(),pjoin(path,f),m.getArtist(),album)
                except: # Probably some tag reader error
                        # Use folder names instead
                    album = path.split(os.path.sep)[-1]
                    artist = path.split(os.path.sep)[-2]
                    title = os.path.splitext(f)[0]
                    trck = track(title,number,pjoin(path,f),artist,album)
                if albums.has_key(album):
                    albums[album].append(trck)
                else:
                    albums[album] = [trck]
    return albums

# - - - - - - - - - - - - - - - - - - - - -

class track:
    def __init__(self,title='',number=0,path='',artist='',album=''):
        self.title=title
        self.number=number
        self.path=path
        self.album=album
        self.artist=artist

    def __str__(self):
        print '%i -- %s' % (self.number,self.title)

class Album2(list):
    def __init__(self,title='',art='',tracks=[]):
        list.__init__(self)
        self.name=title
        self.art=art
        self.artists=[]
        selr.artist=''
        self.addTracks(tracks)

    def __str__(self):
        slist = [self.artist,self.name,'---']+self.tracks
        return string.join(slist,'\n')

    def addTracks(self,tracks):
        for track in tracks:
            if not track.artist in self.artists:
                self.artists.append(track.artist)
            self.append(track)
        self.artist = self.artists[0]
        self.sort(key=attrgetter('number'))

    def findArt(self):
        for track in self.tracks:
            path = track.path



class Album:
    def __init__(self,path='',art=''):
        self.art = art
        self.path = path
        self.name = self.path.split(os.path.sep)[-1]
        self.artist = self.path.split(os.path.sep)[-2]
        self.tracks = None
        self.thumb = None
        self.trackDict = {}
        self.getTracks()

    def __str__(self):
        slist = [self.artist,self.name,'---']+[ t for t.title in self ]
        return string.join(slist,'\n')

    def getTracks(self):
        files = os.listdir(self.path)
        pat = re.compile('.*\.mp3|.*\.flac|.*\.ogg',re.I)
        self.tracks = []
        for (path,dirs,files) in os.walk(self.path):
            self.tracks += sorted(filter(pat.match,files))

    def createThumb(self,targetPath='',size=(300,300)):
        # UGLY! Fix path stuff
        commonPrefixLength = len(os.path.commonprefix((targetPath,self.path)))
        thumbFolder = pjoin(targetPath,self.path[commonPrefixLength:])
        if not os.path.isdir(thumbFolder):
            os.makedirs(thumbFolder)
        self.thumb = pjoin(thumbFolder,self.art)
        if not os.path.exists(self.thumb):
            img = None
            try:
                img = Image.open(pjoin(self.path,self.art))
            except:
                Warn('Cannot open image: %s' % self.art)
            img.resize(size,Image.ANTIALIAS).save(self.thumb)

# - - - - - - - - - - - - - - - - - - - - -

class DJ:
    defaultTopFolder = 'Music'
    defaultRoot = os.getenv('HOME')
    imagePattern = '.*cover.*\.jpg|.*front.*\.jpg|.*cover.*\.jpeg|.*front.*\.jpeg|.*cover.*\.png|.*front.*\.png'
    thumbsFolder = pjoin(defaultRoot,'.coverJuke')
    def __init__(self,root=defaultRoot, topFolder=defaultTopFolder):
        self.root = root
        self.path = pjoin(root,topFolder)
        self.albums = []
        self.nAlbums = len(self.albums)
        self.coverSize = (200,200)
        self.currentAlbum = None
        self.m3uFile = '/tmp/coverPlay.m3u'
        self.turnTable = None

    def update(self,*args,**kwargs):
        self.__init__(*args,**kwargs)

    def setTurnTable(self,t):
        self.turnTable = t

    def findAlbums(self):
        path = self.path
        pat = re.compile(DJ.imagePattern,re.I)
        for (path,dirs,files) in os.walk(path):
            art = filter(pat.match,files)
            if len(art) > 0:
                self.albums.append(Album(path,art[0]))
        self.nAlbums = len(self.albums)

    def collectAlbums(self):
        root = self.path
        albums = {}
        for (path,dirs,files) in os.walk(root):
            for f in files:
                m = metaReader(path,f)
                trck=None
                if m.fileType:
                    album = ''
                    try:
                        m.setReader()
                        trck = track(m.getTitle(),m.getNumber(),pjoin(path,f),m.getArtist(),m.getAlbum())
                    except: # Probably some tag reader error
                            # Use folder names instead
                        album = path.split(os.path.sep)[-1]
                        artist = path.split(os.path.sep)[-2]
                        title = os.path.splitext(f)[0]
                        trck = track(title,number,pjoin(path,f),artist,album)
                    if albums.has_key(album):
                        albums[album].append(trck)
                    else:
                        albums[album] = [trck]
        return albums

    def sortAlbums(self):
        from operator import attrgetter
        self.albums=sorted(self.albums,key=attrgetter('artist'))

    def createThumbs(self):
        for album in self.albums:
            album.createThumb(targetPath=self.thumbsFolder,size=self.coverSize)

    def createPlaylist(self):
        if self.currentAlbum:
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

    def play(self):
        self.createPlaylist()
        self.turnTable.play(self.m3uFile)

    def pause(self):
        self.turnTable.pause()

    def stop(self):
        self.turnTable.stop()

    def next(self):
        self.turnTable.next()

    def prev(self):
        self.turnTable.previous()

    def cleanup(self):
        self.stop()
        self.turnTable.quit()



# - - - - - - - - - - - - - - - - - - - - -

class turnTable:
    ICON_FOLDER = pjoin(DJ.thumbsFolder,'Icons')
    ICON_PLAY = pjoin(ICON_FOLDER,'play_small.png')
    ICON_STOP = pjoin(ICON_FOLDER,'stop_small.png')
    ICON_PAUSE = pjoin(ICON_FOLDER,'pause_small.png')
    ICON_NEXT = pjoin(ICON_FOLDER,'skip-forward_small.png')
    ICON_PREVIOUS = pjoin(ICON_FOLDER,'skip-backward_small.png')
    ICON_EXIT = pjoin(ICON_FOLDER,'quit_small.png')

    def __init__(self):
        self.currentPid = None
        self.isPaused = False

    def signalPlayer(self,signal):
        p = Popen(['kill','-s',signal,str(self.currentPid)])
        p.wait()

# - - - - - - - - - - - - - - - - - - - - -

class mplayerTurnTable(turnTable):
    player = 'mplayer'
    def __init__(self):
        turnTable.__init__(self)

    def play(self, playListFile):
        self.stop()
        p = Popen(['mplayer','-playlist', playListFile])
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

    def next(self):
        pass

    def previous(self):
        pass

# - - - - - - - - - - - - - - - - - - - - -

class dbusTurnTable(turnTable):
    player = ['echo']
    playListArgs = []
    playArgs = ['--play' ]
    stopArgs = ['--stop' ]
    pauseArgs = ['--pause' ]
    nextArgs = ['--fwd']
    previousArgs = ['--rew']
    quitArgs = ['--quit']

    def __init__(self):
        turnTable.__init__(self)

    def play(self,playListFile):
        if not self.isPaused:
            self.quit()
            time.sleep(0.25)
            p = Popen(self.player+self.playListArgs+[playListFile])
            self.currentPid = p.pid
        else:
            Popen(self.player+self.playArgs)
        print self.currentPid
        self.isPaused = False

    def stop(self):
        self.quit()
        #if self.currentPid:
        #    Popen(self.player+self.stopArgs)
        #    self.isPaused = False
        #print self.currentPid

    def pause(self):
        if self.currentPid:
            if not self.isPaused:
                Popen(self.player+self.pauseArgs)
                self.isPaused = True
            else:
                Popen(self.player+self.playArgs)
                self.isPaused = False
        print self.currentPid

    def next(self):
        if self.currentPid:
            Popen(self.player+self.nextArgs)
        print self.currentPid

    def previous(self):
        if self.currentPid:
            Popen(self.player+self.previousArgs)
        print self.currentPid

    def quit(self):
        print self.currentPid
        if self.currentPid:
            self.signalPlayer('KILL')
        self.currentPid = None
        self.isPaused = False


# - - - - - - - - - - - - - - - - - - - - -

class totemTurnTable(dbusTurnTable):
    player = ['totem']
    nextArgs = ['--next']
    previousArgs = ['--previous']
    stopArgs = ['--quit']

    def __init__(self):
        dbusTurnTable.__init__(self)

# - - - - - - - - - - - - - - - - - - - - -

class audaciousTurnTable(dbusTurnTable):
    player = ['audacious', '-i', 'headless']

    def __init__(self):
        dbusTurnTable.__init__(self)



# - - - - - - - - - - - - - - - - - - - - -

class botButtons(wx.Panel):
    def __init__(self,parent,*args,**kwargs):
        wx.Panel.__init__(self,parent,*args,**kwargs)

        global dj

        sizer = wx.GridSizer(rows=1,cols=6)

        quitButton = wx.BitmapButton(self,id=wx.ID_EXIT,bitmap=wx.Bitmap(turnTable.ICON_EXIT))
        #quitButton = wx.Button(self, id=wx.ID_EXIT, label='Quit')
        self.Bind(wx.EVT_BUTTON, self.OnExit, id=wx.ID_EXIT)

        playButton = wx.BitmapButton(self,id=events.ID_PLAY,bitmap=wx.Bitmap(turnTable.ICON_PLAY))
        #playButton = wx.Button(self, id=events.ID_PLAY, label='Play')
        self.Bind(wx.EVT_BUTTON,self.OnPlay,id=events.ID_PLAY)

        pauseButton = wx.BitmapButton(self,id=events.ID_PAUSE,bitmap=wx.Bitmap(turnTable.ICON_PAUSE))
        #pauseButton = wx.Button(self, id=events.ID_PAUSE, label='Pause/Resume')
        self.Bind(wx.EVT_BUTTON,self.OnPause,id=events.ID_PAUSE)

        stopButton = wx.BitmapButton(self,id=events.ID_STOP,bitmap=wx.Bitmap(turnTable.ICON_STOP))
        #stopButton = wx.Button(self, id=events.ID_STOP, label='Stop')
        self.Bind(wx.EVT_BUTTON,self.OnStop,id=events.ID_STOP)

        nextButton = wx.BitmapButton(self,id=events.ID_NEXT,bitmap=wx.Bitmap(turnTable.ICON_NEXT))
        #nextButton = wx.Button(self, id=events.ID_NEXT, label='Next')
        self.Bind(wx.EVT_BUTTON,self.OnNext,id=events.ID_NEXT)

        prevButton = wx.BitmapButton(self,id=events.ID_PREV,bitmap=wx.Bitmap(turnTable.ICON_PREVIOUS))
        #prevButton = wx.Button(self, id=events.ID_PREV, label='Prev')
        self.Bind(wx.EVT_BUTTON,self.OnPrev,id=events.ID_PREV)


        sizer.Add(playButton, flag=wx.ALIGN_LEFT|wx.EXPAND)
        sizer.Add(pauseButton, flag=wx.ALIGN_LEFT|wx.EXPAND)
        sizer.Add(prevButton, flag=wx.ALIGN_LEFT|wx.EXPAND)
        sizer.Add(nextButton, flag=wx.ALIGN_LEFT|wx.EXPAND)
        sizer.Add(stopButton, flag=wx.ALIGN_LEFT|wx.EXPAND)
        sizer.Add(quitButton, flag=wx.ALIGN_RIGHT)

        self.SetSizer(sizer)
        self.Fit()

    def OnPlay(self,e):
        dj.play()

    def OnPause(self,e):
        dj.pause()

    def OnStop(self,e):
        dj.stop()

    def OnNext(self,e):
        dj.next()

    def OnPrev(self,e):
        dj.prev()

    def OnExit(self,e):
        dj.stop()
        dj.cleanup()
        self.Parent.Destroy()


# - - - - - - - - - - - - - - - - - - - - -

class albumCoverPanel(ScrolledPanel):
    def __init__(self,*args,**kwargs):
        ScrolledPanel.__init__(self,*args,**kwargs)

        global dj

        nCoverCols = 3
        nCoverRows = dj.nAlbums/nCoverCols+1
        self.sizer = wx.GridSizer(rows=nCoverRows,cols=nCoverCols,vgap=5,hgap=5)

        self.SetMinSize((nCoverCols*dj.coverSize[0]+55,dj.coverSize[1]))

        for i, album in enumerate(dj.albums):
            ID = events.ID_COVER_START+i
            button = wx.BitmapButton(self,id=ID,bitmap=wx.Bitmap(album.thumb),size=dj.coverSize,name=str(i))
            button.Bind(wx.EVT_BUTTON,self.OnPressCover,id=button.GetId())
            button.Bind(wx.EVT_RIGHT_DOWN,self.OnRightClicCover,id=button.GetId())
            button.Bind(wx.EVT_RIGHT_UP,self.OnRightReleaseCover,id=button.GetId())
            button.SetToolTipString(string.join([album.artist,album.name],'\n'))
            self.sizer.Add(button,flag=wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling(scroll_y=True, scroll_x=False)

    def OnPressCover(self,e):
        b = e.GetEventObject()
        albumIndex = b.GetId()- events.ID_COVER_START
        dj.currentAlbum = dj.albums[albumIndex]
        dj.turnTable.quit()
        dj.play()
        #if dj.albums[albumIndex] == dj.currentAlbum:
        #    dj.turnTable.quit()
        #    dj.play()
        #else:
        #    dj.currentAlbum = dj.albums[albumIndex]
        #    #self.Parent.albumPanel.OnPressCover()

    def OnRightClicCover(self,e):
        b = e.GetEventObject()
        albumIndex = b.GetId()- events.ID_COVER_START
        album = dj.albums[albumIndex]
        b.SetToolTipString(album.__str__())

    def OnRightReleaseCover(self,e):
        b = e.GetEventObject()
        albumIndex = b.GetId()- events.ID_COVER_START
        album = dj.albums[albumIndex]
        b.SetToolTipString(string.join([album.artist,album.name],'\n'))


# - - - - - - - - - - - - - - - - - - - - -

class window0(wx.Frame):
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)

        global dj

        windowWidth,windowHeight = self.GetSize()
        coverWidth,coverHeight = dj.coverSize
        self.sizer = wx.FlexGridSizer(rows=2,cols=1)
        #self.columnsSizer = wx.FlexGridSizer(rows=1,cols=2)

        self.leftBox = wx.StaticBox(self,label='Select Album (%d)' % dj.nAlbums)
        self.leftBoxSizer = wx.StaticBoxSizer(self.leftBox)

        #self.albumPanel = albumInfoPanel(self)
        #self.albumPanel.SetMinSize((2*coverWidth,3*coverHeight))

        self.coverPanel = albumCoverPanel(self)
        self.coverPanel.SetMinSize((3*coverWidth+25,4*coverHeight))

        self.buttonsPanel = botButtons(self)

        self.leftBoxSizer.Add(self.coverPanel,flag=wx.EXPAND)

        #self.columnsSizer.Add(self.leftBoxSizer,flag=wx.EXPAND|wx.ALL,border=10)
        #self.columnsSizer.Add(self.albumPanel,flag=wx.EXPAND|wx.ALL,border=10)

        self.sizer.Add(self.leftBoxSizer,flag=wx.EXPAND)
        self.sizer.Add(self.buttonsPanel,flag=wx.EXPAND)

        self.SetSizerAndFit(self.sizer)
        self.Center()

if __name__=='__main__':
    dj = DJ()

    #grammophone = mplayerTurnTable()
    #grammophone = totemTurnTable()
    grammophone = audaciousTurnTable()
    #grammophone = dbusTurnTable()

    dj.findAlbums()
    print dj.nAlbums
    dj.sortAlbums()
    dj.createThumbs()
    dj.setTurnTable(grammophone)

    app = wx.App()
    mainFrame = window0(None,title='player')
    mainFrame.Show()
    app.MainLoop()

