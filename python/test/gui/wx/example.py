#!/usr/bin/python

# newclass.py

import wx

class NewClass(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer(0, 0)

        text1 = wx.StaticText(panel, -1, 'Java Class')
        sizer.Add(text1, (0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=15)

        icon = wx.StaticBitmap(panel, -1, wx.Bitmap('icons/exec.png'))
        sizer.Add(icon, (0, 4), flag=wx.LEFT,  border=45)

        line = wx.StaticLine(panel, -1 )
        sizer.Add(line, (1, 0), (1, 5), wx.TOP | wx.EXPAND, -15)

        text2 = wx.StaticText(panel, -1, 'Name')
        sizer.Add(text2, (2, 0), flag=wx.LEFT, border=10)

        tc1 = wx.TextCtrl(panel, -1, size=(-1, 30))
        sizer.Add(tc1, (2, 1), (1, 3), wx.TOP | wx.EXPAND, -5)

        text3 = wx.StaticText(panel, -1, 'Package')
        sizer.Add(text3, (3, 0), flag= wx.LEFT | wx.TOP, border=10)

        tc2 = wx.TextCtrl(panel, -1)
        sizer.Add(tc2, (3, 1), (1, 3), wx.TOP | wx.EXPAND, 5)

        button1 = wx.Button(panel, -1, 'Browse...', size=(-1, 30))
        sizer.Add(button1, (3, 4), (1, 1), wx.TOP | wx.LEFT | wx.RIGHT , 5)

        text4 = wx.StaticText(panel, -1, 'Extends')
        sizer.Add(text4, (4, 0), flag=wx.TOP | wx.LEFT, border=10)

        combo = wx.ComboBox(panel, -1, )
        sizer.Add(combo, (4, 1), (1, 3), wx.TOP | wx.EXPAND,  5)

        button2 = wx.Button(panel, -1, 'Browse...', size=(-1, 30))
        sizer.Add(button2, (4, 4), (1, 1), wx.TOP | wx.LEFT | wx.RIGHT , 5)

        sb = wx.StaticBox(panel, -1, 'Optional Attributes')
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        boxsizer.Add(wx.CheckBox(panel, -1, 'Public'), 0, wx.LEFT | wx.TOP, 5)
        boxsizer.Add(wx.CheckBox(panel, -1, 'Generate Default Constructor'), 0,  wx.LEFT, 5)
        boxsizer.Add(wx.CheckBox(panel, -1, 'Generate Main Method'), 0, wx.LEFT | wx.BOTTOM, 5)
        sizer.Add(boxsizer, (5, 0), (1, 5), wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT , 10)
        button3 = wx.Button(panel, -1, 'Help', size=(-1, 30))
        sizer.Add(button3, (7, 0), (1, 1),  wx.LEFT, 10)

        button4 = wx.Button(panel, -1, 'Ok', size=(-1, 30))
        sizer.Add(button4, (7, 3), (1, 1),  wx.LEFT, 10)

        button5 = wx.Button(panel, -1, 'Cancel', size=(-1, 30))
        sizer.Add(button5, (7, 4), (1, 1),  wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)

        sizer.AddGrowableCol(2)
        
        panel.SetSizer(sizer)
        sizer.Fit(self)

        self.Centre()
        self.Show(True)


app = wx.App()
NewClass(None, -1, 'Create Java Class')
app.MainLoop()

