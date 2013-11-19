from wx import *

application = wx.App()

choices = [ 'Red', 'Blue', 'Green', 'Pink', 'White' ]

dialog = wx.SingleChoiceDialog ( None, 'Pick something....', 'Dialog Title', choices )

if dialog.ShowModal() == wx.ID_OK:
   print 'Position of selection:', dialog.GetSelection()
   print 'Selection:', dialog.GetStringSelection()
else:

   print 'You did not select anything.'

dialog.Destroy()
