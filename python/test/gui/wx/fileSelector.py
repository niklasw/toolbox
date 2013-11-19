import wx

# setup the GUI main loop
app = wx.App()

filename = wx.FileSelector()

print filename

app.Destroy()


