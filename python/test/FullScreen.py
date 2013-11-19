#!/usr/bin/python

import pygtk
import gtk
import sys
import gobject

MAX_RETRIES=10


def grab_pointer(gdkwin):
	global MAX_RETRIES
	i =0
	while i<MAX_RETRIES:
		if gtk.gdk.pointer_grab(gdkwin,True)==gtk.gdk.GRAB_SUCCESS:
			return True	
		i+=1
	return False

def grab_keyboard(gdkwin):
	global MAX_RETRIES
	i =0
	while i<MAX_RETRIES:
		if gtk.gdk.keyboard_grab(gdkwin,True)==gtk.gdk.GRAB_SUCCESS:
			return True	
		i+=1
	return False

def createScreenshot():
	rootwindow=gtk.gdk.get_default_root_window()
	width,height=rootwindow.get_size()

	pixbuf=gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,True,8,width,height)

	pixbuf.get_from_drawable(rootwindow,rootwindow.get_colormap(),0,0,0,0,width,height)
	return (width,height,pixbuf)


		



