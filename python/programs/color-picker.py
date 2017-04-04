#!/usr/bin/env python
import pygtk
pygtk.require('3.0')
import gtk

class ColorPicker:
    def close(self, attributes):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.ColorSelectionDialog('Select Color')
        self.window.ok_button.connect("clicked", self.close)
        self.window.cancel_button.connect("clicked", self.close)
        self.window.show()

    def main(self):
        gtk.main()

prog = ColorPicker()
prog.main()
