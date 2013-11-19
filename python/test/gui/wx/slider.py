# experiment with wxPython's wx.Slider
# wx.Slider(parent, id, init_val, min_val, max_val, position_tuple, size_tuple, style)
# position_tuple (x, y) of upper left corner, size_tuple (width, height)
# (on my Windows XP the mouse-wheel controls the slider that has the focus)
# tested with Python24 and wxPython26     vegaseat     17oct2005

import wx

class MyPanel(wx.Panel):
    """
    class MyPanel creates a panel with 2 sliders on it, inherits wx.Panel
    putting your components/widgets on a panel gives additional versatility
    """
    def __init__(self, parent, id):
        # create a panel
        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour("white")

        # wx.SL_VERTICAL  displays the slider vertically
        # wx.SL_HORIZONTAL  displays the slider horizontally
        # wx.SL_AUTOTICKS  displays tick marks
        # wx.SL_LABELS  displays minimum, maximum and value labels
        # initial value = 50, min value = 0, max value = 100
        self.slider1 = wx.Slider(self, -1, 50, 0, 100, (10, 10), (300, 50),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.slider2 = wx.Slider(self, -1, 50, 0, 100, (330, 10), (50, 250),
            wx.SL_VERTICAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        # respond to changes in slider position ...
        self.Bind(wx.EVT_SLIDER, self.sliderUpdate)
        
    def sliderUpdate(self, event):
        self.pos1 = self.slider1.GetValue()
        self.pos2 = self.slider2.GetValue()
        str1 = "pos1 = %d   pos2 = %d" % (self.pos1, self.pos2)
        # display current slider positions in the frame's title
        frame.SetTitle(str1)
        

app = wx.PySimpleApp()
# create a window/frame, no parent, -1 is default ID, title, size
frame = wx.Frame(None, -1, "wxSlider Test1", size = (400, 310))
# call the derived class, -1 is default ID
MyPanel(frame,-1)
# show the frame
frame.Show(True)
# start the event loop
app.MainLoop()
