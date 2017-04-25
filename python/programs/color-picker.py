#!/usr/bin/env python
import pygtk
pygtk.require('3.0')
import gtk

class ColorPicker:
    def close(self, attributes):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.ColorSelectionDialog('Select Color')
        self.window.ok_button.connect("clicked", self.show)
        self.window.cancel_button.connect("clicked", self.close)
        self.window.show()

    def main(self):
        gtk.main()

    def show(self,attributes):
        f = self.window.colorsel.get_current_color()
        colors = [f.red,f.green,f.blue]
        rgb = [int(a/257.0) for a in colors]
        hx = ':'.join([a[2:] for a in map(hex,colors)])
        print 'RGB = {0:02d} {1:02d} {2:02d}'.format(*rgb)
        #print '#{0}'.format(hx)

prog = ColorPicker()
prog.main()
