import os
import wx

MAIN_WINDOW_DEFAULT_SIZE = (300,200)

class Frame(wx.Frame):
    
    def __init__(self, parent, id, title):
        style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER) # XOR to remove the resizeable border        
        wx.Frame.__init__(self, parent, id, title=title, size=MAIN_WINDOW_DEFAULT_SIZE, style=style)
        self.Center() # open in the centre of the screen
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('White') # make the background of the window white

        self.CreateMenuBar()
        
        # create a StatusBar and give it 2 columns
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(2)
        self.statusBar.SetStatusText('No image specified', 1)
        

    def CreateMenuBar(self):
        "Create a menu bar with Open, Exit items"
        menuBar = wx.MenuBar()
        # Tell our Frame about this MenuBar
        self.SetMenuBar(menuBar)
        menuFile = wx.Menu()
        menuBar.Append(menuFile, '&File')
        # NOTE on wx ids - they're used everywhere, we don't care about them
        # Used to handle events and other things
        # An id can be -1 or wx.ID_ANY, wx.NewId(), your own id
        # Get the id using object.GetId()
        fileOpenMenuItem = menuFile.Append(-1, '&Open Image', 'Open a picture')
        #print "fileOpenMenuItem.GetId()", fileOpenMenuItem.GetId()
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpenMenuItem)

        # add a 'mirror' option, disable it for now
        # we add mirrorMenuItem to self so that we can reference it later
        #self.mirrorMenuItem = menuFile.Append(-1, '&Mirror Image', 'Mirror the image horizontally')
        #self.mirrorMenuItem.Enable(False) # we can't mirror an image until we've loaded one in, so start with 'mirror' disabled
        #self.Bind(wx.EVT_MENU, self.OnMirrorImage, self.mirrorMenuItem)
        
        # create a menu item for Exit and bind it to the OnExit function       
        exitMenuItem = menuFile.Append(-1, 'E&xit', 'Exit the viewer')        
        self.Bind(wx.EVT_MENU, self.OnExit, exitMenuItem)
        
        # add a Help menu with an About item
        #menuHelp = wx.Menu()
        #menuBar.Append(menuHelp, '&Help')
        #helpMenuItem = menuHelp.Append(-1, '&About', 'About screen')
        #self.Bind(wx.EVT_MENU, self.OnAbout, helpMenuItem)

    def OnOpen(self, event):
        "Open an image file, set title if successful"
        # Create a file-open dialog in the current directory
        
        filters = 'Image files (*.gif;*.png;*.jpg)|*.gif;*.png;*.jpg'
        dlg = wx.FileDialog(self, message="Open an Image...", defaultDir=os.getcwd(), 
                            defaultFile="", wildcard=filters, style=wx.OPEN)
        
        # Call the dialog as a model-dialog so we're required to choose Ok or Cancel
        if dlg.ShowModal() == wx.ID_OK:
            # User has selected something, get the path, set the window's title to the path
            filename = dlg.GetPath()
            self.SetTitle(filename)
            wx.BeginBusyCursor()            
            #self.image = wx.Image(filename, wx.BITMAP_TYPE_ANY, -1) # auto-detect file type        
            #self.statusBar.SetStatusText('Size = %s' % (str(self.image.GetSize())), 1)
            #self.ShowBitmap()
            wx.EndBusyCursor()
                        
        dlg.Destroy() # we don't need the dialog any more so we ask it to clean-up

    def ShowBitmap(self):
        # NOTE doesn't delete old bitmap which can cause a memory leak!
        
        # Convert to Bitmap for wxPython to draw it to screen
        self.bitmap = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.image))       
        # Make the application's window as large as the image
        self.SetClientSize(self.bitmap.GetSize())
        #self.Center() # open in the centre of the screen
        
    def OnExit(self, event):
        "Close the application by Destroying the object"
        self.Destroy() 
        
    
class App(wx.App):
    
    def OnInit(self):
        self.frame = Frame(parent=None, id=-1, title='Image Viewer')
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
    
if __name__ == "__main__":       
    # make an App object, set stdout to the console so we can see errors
    app = App(redirect=False)
        
    app.MainLoop()
