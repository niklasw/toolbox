#!/usr/bin/python

import wx,os,sys,re
from subprocess import Popen

class events:
    ID_FILE_TXT = 10
    ID_CANCEL = 20
    ID_SUBMIT = 25
    ID_FILESELECT = 30

class dataContainer:
    selectedFile=''
    nCpus=0
    useMaster=False
    ram=8

class mainWindow(wx.Frame):
    def __init__(self,parent,id,title,size=(800,300)):
        wx.Frame.__init__(self,parent,id,title,size=size)

        global DATA
        global EVENTS

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        menubar.Append(fileMenu,'&File')
        self.SetMenuBar(menubar)

        # ------------------------------

        panel = wx.Panel(self,-1,name='Panel')
        panel.SetBackgroundColour('grey')

        sizer = wx.FlexGridSizer(rows=3,cols=2)
        cpuBox =  wx.StaticBox(panel, -1, 'Requirements')
        cpuBoxSizer = wx.StaticBoxSizer(cpuBox, wx.VERTICAL)
        optBox = wx.StaticBox(panel, -1, 'Optional Attributes')
        optBoxSizer = wx.StaticBoxSizer(optBox, wx.VERTICAL)
        fileBox = wx.StaticBox(panel, -1, 'Select case file')
        fileBoxSizer = wx.StaticBoxSizer(fileBox, wx.HORIZONTAL)

        panel.SetSizer(sizer)

        # ------------------------------

        self.fileSelectButton = wx.Button(panel,EVENTS.ID_FILESELECT,'Browse')
        self.caseFileSelectorTxt = wx.TextCtrl(panel, EVENTS.ID_FILE_TXT, DATA.selectedFile, size=(200,30))

        self.numCpuSlider = wx.Slider(panel,-1,value=4,minValue=1,maxValue=128, size=(200,30), style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.memSlider = wx.Slider(panel,-1,value=4,minValue=24,maxValue=128, size=(200,30), style=wx.SL_AUTOTICKS | wx.SL_LABELS)

        self.masterNode = wx.CheckBox(panel, -1, label='Use Master node')
        self.masterNode.SetValue(True)
        self.submit = wx.CheckBox(panel, -1, label='Submit to cluster')
        self.submit.SetValue(False)

        cancelButton = wx.Button(panel, EVENTS.ID_CANCEL, 'Close')

        submitButton = wx.Button(panel,EVENTS.ID_SUBMIT, 'Submit')

        # ----
        fileBoxSizer.Add(self.caseFileSelectorTxt)
        fileBoxSizer.Add(self.fileSelectButton,wx.ALIGN_RIGHT)
        sizer.Add(fileBoxSizer,wx.EXPAND)

        # ----
        sizer.Add(wx.StaticLine(panel))

        # ----
        optBoxSizer.Add(self.masterNode,proportion=0,flag=wx.LEFT|wx.CENTER,border=5)
        optBoxSizer.Add(self.submit,proportion=0,flag=wx.LEFT|wx.CENTER,border=5)
        sizer.Add(optBoxSizer,wx.EXPAND|wx.ALIGN_CENTER)

        # ----
        cpuBoxSizer.Add(self.numCpuSlider,wx.EXPAND)
        cpuBoxSizer.Add(wx.StaticText(panel,-1,'Number of CPU\'s'),wx.EXPAND)
        cpuBoxSizer.Add(wx.StaticLine(panel,-1),wx.EXPAND)
        cpuBoxSizer.Add(self.memSlider,wx.EXPAND)
        cpuBoxSizer.Add(wx.StaticText(panel,-1,'Memory requirement'),wx.EXPAND)
        sizer.Add(cpuBoxSizer,0,wx.EXPAND,0)

        # ----
        sizer.Add(cancelButton)
        sizer.Add(submitButton)

        self.Centre()
        self.Show(True)

        wx.EVT_BUTTON(self,EVENTS.ID_FILESELECT,self.OnFileSelect)
        wx.EVT_BUTTON(self,EVENTS.ID_CANCEL,self.OnCancel)
        wx.EVT_BUTTON(self,EVENTS.ID_SUBMIT,self.OnSubmit)
        self.Bind(wx.EVT_SLIDER, self.sliderUpdate)

    def sliderUpdate(self,e):
        DATA.nCpus = self.numCpuSlider.GetValue()
        DATA.ram = self.memSlider.GetValue()
        pass

    def OnSubmit(self,e):
        fptr = open('case.job','w')
        fptr.write('%s\n' % DATA.selectedFile)
        fptr.write('%d\n' % DATA.ram)
        fptr.write('%d\n' % DATA.nCpus)
        fptr.close()
        Popen(['gedit','case.job'])
        self.Destroy()

    def OnCancel(self,e):
        self.Destroy()

    def OnFileSelect(self,e):
        DATA.selectedFile = wx.FileSelector(parent=self,default_path=os.getcwd())
        self.caseFileSelectorTxt.SetValue(DATA.selectedFile)
        DATA
        self.Refresh()


DATA = dataContainer()
EVENTS = events()

app = wx.App()
mainFrame = mainWindow(None,-1,'Qsub')
app.MainLoop()

