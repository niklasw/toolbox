#!/usr/bin/python
# -*- encoding: UTF-8 -*-
#

import wx
from wx.lib.scrolledpanel import ScrolledPanel
import os,re,sys,Image,string,time
from os.path import join as pjoin
from subprocess import Popen

from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.oggvorbis import OggVorbis
from operator import attrgetter

def Warn(s):
    print "Warning: %s" % s

class configuration(dict):
    confPath = pjoin(os.getenv('HOME'),'.coverJuke')
    confFile = pjoin(confPath,'config')
    def __init__(self):
        dict.__init__(self)
        self.read()
        self['coverTileWidth'] = 4
        self['coverWidth'] = 200
        self['coverHeight'] = 200
        self['musicRoot'] = pjoin(os.getenv('HOME'),'Music')
        self['name'] = 'CoverJuke'

    def read(self):
        f = open(self.confFile,'r')
        line=''
        for line in f:
            line=line.strip()
            if line[0] == '#':
                continue
            try:
                key,tmp = map(string.strip,line.split('='))
                try:
                    val=int(tmp)
                except:
                    val=tmp
            except:
                Warn('Config read error')
                continue
            self[key] = val

    def __str__(self):
        out = '#Config:\n'
        for key,val in self.iteritems():
            out += "%s=%s\n" %( key,val )
        return out

    def write(self):
        file(self.confFile,'w').write(self.__str__())

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
    ID_LETTER_START = 1000

# - - - - - - - - - - - - - - - - - - - - -

class metaReader(dict):
    knownExtensions = ['OGG','FLAC','MP3']
    albumTag = 'album'
    artistTag = 'artist'
    albumArtistTag = 'artistsort'
    titleTag = 'title'
    numberTag = 'tracknumber'
    def __init__(self,filePath=''):
        dict.__init__(self)
        self.file=filePath
        if self.file: self.getFiletypeByExtension()
        self.reader = None
        self.isAudio = False

    def getFiletypeByExtension(self):
        EXT = (os.path.splitext(self.file)[-1]).upper().strip('.')
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
        s = string.join(item,sep)
        return s

    def getAlbum(self,default='Unknown Album'):
        try:
            out = self.l2s(self.reader[self.albumTag])
        except:
            out = default
        return out

    def getAlbumArtist(self, default='Unknown Album Artist'):
        try:
            if self.albumArtistTag in self.reader.keys():
                out = self.l2s(self.reader[self.albumArtistTag])
            else:
                out = self.getArtist(default)
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
class track:
    def __init__(self,title='',number=0,path='',artist='',album=''):
        self.title=title
        self.number=number
        self.path=path
        self.album=album
        self.artist=artist

    def __str__(self):
        return '%3i - %s' % (self.number,self.title)


class Album:
    def __init__(self,path='',art=''):
        self.art = art
        self.path = path
        self.name = self.path.split(os.path.sep)[-1]
        self.artist = self.path.split(os.path.sep)[-2]
        self.tracks = []
        self.files = []
        self.thumb = None
        self.getTracks()
        self.getName()

    def __str__(self):
        return fullInfo()

    def fullInfo(self,markIndex=-1):
        trackInfo = [ a.__str__() for a in self.tracks ]
        marks = [' ']*len(trackInfo)
        if markIndex >= 0: marks[markIndex] = '*'
        trackInfo =  map(string.join, zip(marks,trackInfo))
        return string.join([self.artist,self.name,'---']+trackInfo,'\n')

    def shortInfo(self):
        return string.join([self.artist,self.name],'\n')

    def getTracks(self):
        files = os.listdir(self.path)
        pat = re.compile('.*\.mp3|.*\.flac|.*\.ogg',re.I)
        for (path,dirs,files) in os.walk(self.path):
            addPath = lambda f:os.path.join(path,f)
            self.files += map(addPath, filter(pat.match,files))
        for i,f in enumerate(self.files):
            m = metaReader(f)
            m.getFiletypeByExtension()
            if m.isAudio:
                m.setReader()
                t = track(path=f)
                t.title = m.getTitle(default = os.path.basename(f))
                t.number = m.getNumber(default=i)
                t.album = m.getAlbum(default=u'Unknown Album')
                t.artist = m.getAlbumArtist(default=u'Unknown Artist')
                self.tracks.append(t)
        self.tracks.sort(key=attrgetter('number'))

    def getName(self):
        self.name = self.tracks[0].album
        self.artist = self.tracks[0].artist

    def createThumb(self,targetPath='',size=(300,300), recreate=False):
        # UGLY! Fix path stuff
        commonPrefixLength = len(os.path.commonprefix((targetPath,self.path)))
        thumbFolder = pjoin(targetPath,self.path[commonPrefixLength:])
        if not os.path.isdir(thumbFolder):
            os.makedirs(thumbFolder)
        self.thumb = pjoin(thumbFolder,self.art)
        if not os.path.exists(self.thumb) or recreate:
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
    #def __init__(self,root=defaultRoot, topFolder=defaultTopFolder):
    def __init__(self, config):
        self.config = config
        self.path = config['musicRoot']
        self.albums = []
        self.nAlbums = len(self.albums)
        self.coverSize = (config['coverWidth'],config['coverHeight'])
        self.tile = (config['coverTileWidth'],config['coverTileHeight'])
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

    def sortAlbums(self):
        self.albums=sorted(self.albums,key=attrgetter('artist'))

    def getAlbumIndexByLetter(self,letter):
        index = 0
        for i,album in enumerate(self.albums):
            if album.artist[0].upper() == letter.upper():
                return index
            index += 1
        return index

    def getAlbumIndexByName(self,name):
        albumNames = [a.name for a in  self.albums]
        if name in albumNames:
            return albumNames.index(name)
        else:
            return -1

    def getCurrentAlbumIndex(self):
        if self.currentAlbum:
            return self.getAlbumIndexByName(self.currentAlbum.name)
        else:
            return -1

    def createThumbs(self):
        for album in self.albums:
            album.createThumb(targetPath=self.thumbsFolder,size=self.coverSize,recreate=self.config['recreateThumbs'])

    def createPlaylist(self):
        if self.currentAlbum:
            album = self.currentAlbum
            hdr = '#EXTM3U'
            lines = [hdr]
            for track in album.tracks:
                lines.append(track.path)
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

    KEY_PAUSE = ','
    KEY_STOP = '.'

    def __init__(self):
        self.currentPid = None
        self.isPaused = False
        self.currentTrackIndex = 0

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

    def next(self):
        if self.currentPid:
            self.currentTrackIndex += 1
            Popen(self.player+self.nextArgs)

    def previous(self):
        if self.currentPid:
            self.currentTrackIndex -= 1
            Popen(self.player+self.previousArgs)

    def quit(self):
        if self.currentPid:
            self.signalPlayer('KILL')
        self.currentTrackIndex = 0
        self.currentPid = None
        self.isPaused = False


# - - - - - - - - - - - - - - - - - - - - -

class totemTurnTable(dbusTurnTable):
    player = ['totem']
    nextArgs = ['--next']
    previousArgs = ['--previous']
    stopArgs = ['--quit']
    pauseArgs = ['--play-pause' ]

    def __init__(self):
        dbusTurnTable.__init__(self)

# - - - - - - - - - - - - - - - - - - - - -

class audaciousTurnTable(dbusTurnTable):
    player = ['audacious', '-i', 'headless']

    def __init__(self):
        dbusTurnTable.__init__(self)

# - - - - - - - - - - - - - - - - - - - - -

class albumCoverPanel(ScrolledPanel):
    vGap = 5
    hGap = 5
    def __init__(self,*args,**kwargs):
        ScrolledPanel.__init__(self,*args,**kwargs)

        global dj

        self.SetBackgroundColour('#222233')
        nCoverCols = dj.tile[0]
        nCoverRows = dj.nAlbums/nCoverCols+1
        self.tile = (nCoverCols,nCoverRows)
        self.scrollStepsPerAlbum = 5
        self.scrollStepSize = (dj.coverSize[1]+self.vGap)/self.scrollStepsPerAlbum

        self.sizer = wx.GridSizer(rows=nCoverRows,cols=self.tile[0],vgap=self.vGap) #,hgap=self.hGap)

        self.SetMinSize((nCoverCols*dj.coverSize[0]+100,dj.coverSize[1]))

        for i, album in enumerate(dj.albums):
            ID = events.ID_COVER_START+i
            button = wx.BitmapButton(self,id=ID,bitmap=wx.Bitmap(album.thumb),size=dj.coverSize,name=str(i))
            button.Bind(wx.EVT_BUTTON,self.OnPressCover,id=button.GetId())
            button.Bind(wx.EVT_RIGHT_DOWN,self.OnRightClicCover,id=button.GetId())
            button.Bind(wx.EVT_RIGHT_UP,self.OnRightReleaseCover,id=button.GetId())
            button.SetToolTipString(album.shortInfo())
            self.sizer.Add(button,flag=wx.ALIGN_CENTER)

        self.SetSizer(self.sizer)
        self.SetFocus()
        self.SetAutoLayout(1)

        self.Bind(wx.EVT_SIZE,self.OnResize)

        self.SetupScrolling(scroll_y=True, scroll_x=False,rate_y=self.scrollStepSize)


    def OnPressCover(self,e):
        b = e.GetEventObject()
        albumIndex = b.GetId()- events.ID_COVER_START
        dj.currentAlbum = dj.albums[albumIndex]
        dj.turnTable.quit()
        self.Parent.SetTitle('%s || %s: %s' % (dj.config['name'],dj.currentAlbum.artist,dj.currentAlbum.name))
        dj.play()

    def OnRightClicCover(self,e):
        b = e.GetEventObject()
        albumIndex = b.GetId()- events.ID_COVER_START
        album = dj.albums[albumIndex]
        b.SetFocus()
        markIndex = -1
        if dj.currentAlbum:
            if albumIndex == dj.getCurrentAlbumIndex():
                markIndex = dj.turnTable.currentTrackIndex
        b.SetToolTipString(album.fullInfo(markIndex))

    def OnRightReleaseCover(self,e):
        b = e.GetEventObject()
        albumIndex = b.GetId()- events.ID_COVER_START
        album = dj.albums[albumIndex]
        b.SetToolTipString(string.join([album.artist,album.name],'\n'))

    def scrollLines(self,n):
        self.ScrollLines(n*self.scrollStepsPerAlbum)

    def scrollToLine(self,n):
        self.Scroll(x=0,y=n*self.scrollStepsPerAlbum)

    def scrollToArtist(self,name):
        pass

    def scrollToAlbum(self,title):
        pass

    def OnResize(self,e):
        size = e.GetSize()
        nCols = size[0]/dj.coverSize[0]
        self.tile = (nCols,dj.nAlbums/nCols+1)
        self.sizer.SetCols(nCols)

# - - - - - - - - - - - - - - - - - - - - -

class window0(wx.Frame):
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)

        global dj

        windowWidth,windowHeight = self.GetSize()
        coverWidth,coverHeight = dj.coverSize

        self.coverPanel = albumCoverPanel(self)

        self.coverPanel.SetMinSize(
                    (dj.tile[0]*(coverWidth+2*albumCoverPanel.hGap),
                     dj.tile[1]*(coverHeight+2*albumCoverPanel.vGap)))
        self.SetMinSize(
                    (dj.tile[0]*(coverWidth+2*albumCoverPanel.hGap),
                     dj.tile[1]*(coverHeight+2*albumCoverPanel.vGap)))

        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        self.Fit()
        self.Center()

    def OnFullScreen(self,event):
        self.ShowFullScreen(not self.IsFullScreen())

    def OnKeyUp(self,e):
        letters='ABCDEFGHIJKLMNOPQRSTUVXYZ'

        keycode = e.GetKeyCode()

        print 'Pressed key code',keycode

        if keycode == wx.WXK_ESCAPE:
           ret  = wx.MessageBox('Are you sure to quit?', 'Question', wx.YES_NO | wx.CENTRE | wx.YES_DEFAULT, self)
           if ret == wx.YES:
               self.Close()
           e.Skip()
        elif keycode == wx.WXK_UP:
            self.coverPanel.scrollLines(-1)
        elif keycode == wx.WXK_DOWN:
            self.coverPanel.scrollLines(1)
        elif keycode == wx.WXK_RIGHT:
            dj.next()
        elif keycode == wx.WXK_LEFT:
            dj.prev()
        elif keycode == wx.WXK_F11:
            self.OnFullScreen(e)
        elif keycode == ord(turnTable.KEY_PAUSE):
            dj.pause()
        elif keycode == ord(turnTable.KEY_STOP):
            dj.stop()
        elif keycode in map(ord,letters):
            albumIndex= dj.getAlbumIndexByLetter(chr(keycode))
            scrollY = albumIndex/self.coverPanel.tile[0]
            self.coverPanel.scrollToLine(scrollY)
        print dj.turnTable.currentTrackIndex

if __name__=='__main__':
    conf = configuration()
    conf.read()

    dj = DJ(conf)
    print conf

    #grammophone = mplayerTurnTable()
    #grammophone = dbusTurnTable()
    #grammophone = totemTurnTable()
    grammophone = audaciousTurnTable()

    dj.findAlbums()
    dj.sortAlbums()
    dj.createThumbs()
    dj.setTurnTable(grammophone)

    app = wx.App()
    mainFrame = window0(None,title=conf['name'])
    mainFrame.Show()
    app.MainLoop()
    dj.cleanup()

