#!/usr/bin/python

# colordepth.py

import wx

ID_DEPTH = 1
ID_256 = 256
ID_16 = 16
ID_TXT = 2
ID_OK = 3
ID_CANCEL = 4

class ChangeDepth(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(250, 210))

        self.result=''

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        panel = wx.Panel(self, -1,size=(225,190))

        wx.StaticBox(panel, -1, 'Colors')
        hbox.Add(static,1,wx.EXPAND)
        self.radioBtns = []
        self.radioBtns.append(wx.RadioButton(panel, -1, '256 Colors', (15, 30), style=wx.RB_GROUP))
        self.radioBtns.append(wx.RadioButton(panel, -1, '16 Colors', (15, 55)))
        self.radioBtns.append(wx.RadioButton(panel, -1, '2 Colors', (15, 80)))
        self.radioBtns.append(wx.RadioButton(panel, -1, 'Custom', (15, 105)))
        self.radioBtns[3].SetValue(True)

        self.inputText = wx.TextCtrl(panel, ID_TXT, 'Hejhej', (95, 105))

        okButton = wx.Button(self, ID_OK, 'Ok', size=(70, 30))
        closeButton = wx.Button(self, ID_CANCEL, 'Cancel', size=(70, 30))
        hbox.Add(okButton, 1,wx.RIGHT)
        hbox.Add(closeButton, 1, wx.LEFT)

        vbox.Add(panel,1, wx.EXPAND)
        vbox.Add(hbox, 1, wx.EXPAND)

        wx.EVT_BUTTON(self,ID_OK,self.OnOK)
        wx.EVT_BUTTON(self,ID_CANCEL,self.OnCancel)

        self.SetSizer(vbox)

    def OnOK(self,e):
        choice=False
        for radio in self.radioBtns:
            if radio.GetValue():
                if 'Custom' == radio.GetLabelText():
                    self.result =  self.inputText.GetValue()
                else:
                    self.result =  radio.GetLabelText()
        self.Destroy()

    def OnCancel(self,e):
        self.Destroy()

class ColorDepth(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(350, 220))

        menubar = wx.MenuBar()
        file = wx.Menu()
        edit = wx.Menu()
        help = wx.Menu()

        menubar.Append(file, '&File')
        menubar.Append(edit, '&Edit')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)

        toolbar = self.CreateToolBar()
        toolbar.AddLabelTool(ID_DEPTH, 'Pressme', wx.Bitmap('icons/color.png'))
        self.Bind(wx.EVT_TOOL, self.OnChangeDepth, id=ID_DEPTH)

        panel = wx.Panel(self, -1, size= (200,100))
        panel.SetBackgroundColour('#4f5049')

        sizer = wx.GridSizer(rows=3,cols=2,vgap=8,hgap=8)
        inputText = wx.TextCtrl(panel, ID_TXT, 'Hejhej')
        closeButton = wx.Button(panel, ID_CANCEL, 'Close')

        spacer = wx.Panel(panel, -1, size=(100,20))

        sizer.Add(inputText,1,wx.EXPAND|wx.TOP)
        sizer.Add(closeButton,1,wx.EXPAND|wx.BOTTOM)
        sizer.Add(closeButton,1,wx.EXPAND|wx.BOTTOM)
        sizer.Add(spacer,1,wx.EXPAND)
        sizer.Add(spacer,1,wx.EXPAND)
        sizer.Add(spacer,1,wx.EXPAND)

        panel.SetSizer(sizer)

        self.Centre()
        self.Show(True)
        wx.EVT_BUTTON(self,ID_CANCEL,self.OnCancel)

    def OnCancel(self,e):
        self.Destroy()

    def OnChangeDepth(self, event):
        chgdep = ChangeDepth(None, -1, 'Change Color Depth',)
        chgdep.ShowModal()
        print chgdep.result
        chgdep.Destroy()

app = wx.App()
ColorDepth(None, -1, '')
app.MainLoop()

