#!/usr/bin/python

import wx,os,sys,re,string
from subprocess import Popen

class events:
    ID_FILE_TXT = 10
    ID_SUBMIT = 25
    ID_FILESELECT = 30
    ID_JID_ADD = 40

class dataContainer(dict):
    def __init__(self,*args,**kwargs):
        dict.__init__(self,*args,**kwargs)
        self['Case file'] = ''
        self['N CPU'] = 4
        self['Use Master node'] = True
        self['Submit to cluster'] = True
        self['RAM'] = 4
        self['Radio options'] = ''
        self['Hold jid'] = []

class Qstat:
    def __init__(self):
        self.myJids = self.getJids()
        self.allJids = self.getJids(all=True)

    def getJids(self,type=int,all=False):
        return map(type,[1234, 2345,2346,2347,2358,2563])

class botButtons(wx.Panel):
    def __init__(self,parent,*args,**kwargs):
        wx.Panel.__init__(self,parent,*args,**kwargs)

        global DATA
        global EVENTS

        self.SetBackgroundColour('grey')

        sizer = wx.GridSizer(rows=1,cols=2)

        cancelButton = wx.Button(self, id=wx.ID_CANCEL, label='Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)

        submitButton = wx.Button(self, id=EVENTS.ID_SUBMIT, label='Submit')
        self.Bind(wx.EVT_BUTTON,self.OnSubmit,id=EVENTS.ID_SUBMIT)

 
        sizer.Add(cancelButton)
        sizer.Add(submitButton, flag=wx.ALIGN_RIGHT)

        self.SetSizer(sizer)
        self.Fit()

    def OnSubmit(self,e):
        resultsDialog = infoDialog(parent=None, title='You have selected',size=(300,600))
        resultsDialog.ShowModal()
        resultsDialog.Destroy()

    def OnCancel(self,e):
        self.Parent.Destroy()


class qstatPanel(wx.Panel):
    def __init__(self,parent,*args,**kwargs):
        wx.Panel.__init__(self,parent,*args,**kwargs)

        global DATA
        global EVENTS

        self.SetBackgroundColour('grey')

        sizer = wx.FlexGridSizer(rows=3,cols=1)
        self.holdBox = wx.StaticBox(self, label='Hold jobs')
        self.boxSizer = wx.StaticBoxSizer(self.holdBox,wx.VERTICAL)
        self.holdSizer = wx.FlexGridSizer(rows=1,cols=2)

        clearButton = wx.Button(self,id=-1,label='Clear')

        # --hold-jid ------------------
        q = Qstat()
        self.jobListBox = wx.ListBox(self,choices=q.getJids(type=str),style=wx.LB_MULTIPLE|wx.LB_SORT)

        self.Bind(wx.EVT_BUTTON,self.OnAddJid)
        self.Bind(wx.EVT_LISTBOX,self.OnAddJid)
        self.Bind(wx.EVT_BUTTON,self.OnClearButton)

        self.holdInfoText = wx.StaticText(self,label='None', size=(100,100))
        self.holdSizer.Add(self.holdInfoText)
        self.holdSizer.Add(self.jobListBox,wx.EXPAND)
        self.boxSizer.Add(self.holdSizer)
        sizer.Add(self.boxSizer,flag=wx.EXPAND)
        sizer.Add(clearButton,flag=wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(sizer)

        self.Fit()
        # ------------------------------

    def OnAddJid(self,e):
        l = e.GetEventObject()
        selections = l.GetSelections()
        choices = l.GetItems()
        vals = []
        for i in selections: vals.append(choices[i])
        DATA['Hold jid']=vals
        print DATA['Hold jid']
        text = 'Selection:\n'+string.join(vals,'\n')
        self.holdInfoText.SetLabel(text)

    def OnClearButton(self,e):
        self.jobListBox.SetSelection(-1)
        self.holdInfoText.SetLabel('None')


class filePanel(wx.Panel):
    def __init__(self,parent,*args,**kwargs):
        wx.Panel.__init__(self,parent,*args,**kwargs)

        global DATA
        global EVENTS

        self.SetBackgroundColour('grey')

        sizer = wx.FlexGridSizer(rows=1,cols=2)

        fileBox = wx.StaticBox(self, label='Case file')
        fileBoxSizer = wx.StaticBoxSizer(fileBox, wx.HORIZONTAL)

        self.fileSelectButton = wx.Button(self,id=EVENTS.ID_FILESELECT,label='Select case file')
        self.caseFileSelectorTxt = wx.TextCtrl(self,id=EVENTS.ID_FILE_TXT, name='Case file', value=DATA['Case file'], size=(300,30))
        self.Bind(wx.EVT_BUTTON,self.OnFileSelect,id=EVENTS.ID_FILESELECT)

        fileBoxSizer.Add(self.caseFileSelectorTxt)
        fileBoxSizer.Add(self.fileSelectButton,wx.ALIGN_RIGHT)

        sizer.Add(fileBoxSizer)

        self.SetSizer(sizer)
        self.Fit()

    def OnFileSelect(self,e):
        DATA['Case file'] = wx.FileSelector(parent=self,default_path=os.getcwd())
        self.caseFileSelectorTxt.SetValue(DATA['Case file'])


class mainPanel(wx.Panel):
    def __init__(self,parent,*args,**kwargs):
        wx.Panel.__init__(self,parent,*args,**kwargs)

        global DATA
        global EVENTS

        self.SetBackgroundColour('grey')

        sizer = wx.GridSizer(rows=3,cols=2)
        cpuBox =  wx.StaticBox(self, label='Requirements')
        cpuBoxSizer = wx.StaticBoxSizer(cpuBox, wx.VERTICAL)
        optBox = wx.StaticBox(self, label='Optional Attributes')
        optBoxSizer = wx.StaticBoxSizer(optBox, wx.VERTICAL)

        self.SetSizer(sizer)

        # Resource allocation --------
        self.numCpuSlider = wx.Slider(self,name='N CPU',value=DATA['N CPU'],minValue=1,maxValue=128, size=(200,30), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
        self.numCpuSlider.SetTickFreq(4,pos=1)
        self.memSlider = wx.Slider(self,name='RAM',value=DATA['RAM'],minValue=DATA['RAM'],maxValue=128, size=(200,30), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
        self.Bind(wx.EVT_SLIDER, self.sliderUpdate)

        # Options --------------------
        self.masterNode = wx.CheckBox(self, label='Use Master node')
        self.masterNode.SetValue(DATA['Use Master node'])
        self.submit = wx.CheckBox(self, label='Submit to cluster')
        self.submit.SetValue(DATA['Submit to cluster'])
        self.Bind(wx.EVT_CHECKBOX,self.OnCheckBox)

        r = self.radioBox = wx.RadioBox(self,label='Radio options',style=wx.VERTICAL,choices=['One','Two','Three'])
        self.Bind(wx.EVT_RADIOBOX,self.OnRadiobox)

        # ----
        optBoxSizer.Add(self.masterNode,proportion=0,flag=wx.LEFT|wx.CENTER,border=5)
        optBoxSizer.Add(self.submit,proportion=0,flag=wx.LEFT|wx.CENTER,border=5)
        optBoxSizer.Add(self.radioBox,flag=wx.LEFT,border=8)
        sizer.Add(optBoxSizer,wx.EXPAND|wx.ALIGN_CENTER)

        # ----
        cpuBoxSizer.Add(self.numCpuSlider,wx.EXPAND)
        cpuBoxSizer.Add(wx.StaticText(self,-1,'Number of CPU\'s'),wx.EXPAND)
        cpuBoxSizer.Add(wx.StaticLine(self,-1),wx.EXPAND)
        cpuBoxSizer.Add(self.memSlider,wx.EXPAND)
        cpuBoxSizer.Add(wx.StaticText(self,-1,'Memory requirement'),wx.EXPAND)
        sizer.Add(cpuBoxSizer,0,wx.EXPAND|wx.ALIGN_RIGHT,0)


        self.Fit()
        # ------------------------------

    def OnCheckBox(self,e):
        c=e.GetEventObject()
        DATA[c.GetLabelText()] = c.GetValue()

    def sliderUpdate(self,e):
        s=e.GetEventObject()
        DATA[s.GetName()] = s.GetValue()

    def OnRadiobox(self,e):
        r = e.GetEventObject()
        DATA[r.GetLabelText()] = r.GetStringSelection()

class infoDialog(wx.Dialog):
    def __init__(self,*args,**kwargs):
        wx.Dialog.__init__(self,*args,**kwargs)
        global DATA

        sizer=wx.FlexGridSizer(rows=3,cols=1,vgap=15,hgap=15)
        for key in DATA.keys():
            sizer.Add( wx.StaticText(self, label= 'Value of %s : %s' % ( key, DATA[key]),style=wx.EXPAND ))
        self.SetSizer(sizer)
        self.Center()
        self.Fit()

class mainWindow(wx.Frame):
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)

        global DATA
        global EVENTS

        #menubar = wx.MenuBar()
        #fileMenu = wx.Menu()
        #menubar.Append(fileMenu,'&File')
        #self.SetMenuBar(menubar)

        # ------------------------------

        sizer = wx.FlexGridSizer(rows=3,cols=1)

        box = wx.StaticBox(self, label='Case file')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        self.Panel0 = filePanel(self)
        self.Panel1 = mainPanel(self)
        self.Panel2 = qstatPanel(self)
        self.Panel3 = botButtons(self)

        sizer.Add(self.Panel0,flag=wx.EXPAND)
        sizer.Add(self.Panel1,flag=wx.EXPAND)
        sizer.Add(self.Panel2,flag=wx.EXPAND)
        sizer.Add(self.Panel3,flag=wx.EXPAND)

        boxSizer.Add(sizer,flag=wx.ALL, border=5)
        # ------------------------------

        self.SetSizer(boxSizer)
        self.Center()
        self.Fit()


DATA = dataContainer()
EVENTS = events()

app = wx.App()
mainFrame = mainWindow(None,title='Qsub',size=(800,300))
mainFrame.Show()
app.MainLoop()

