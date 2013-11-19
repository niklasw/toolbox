#!/usr/bin/python

import gtk,sys

def quit(b):
    sys.exit(0)

def addBtn(box, title, signal, call):
    btn=gtk.Button(title)
    btn.connect(signal,call)
    box.add(btn)

def mkBox(horizontal=True,spacing=0,layout=gtk.BUTTONBOX_SPREAD):
    if horizontal:
        bbox = gtk.HButtonBox()
    else:
        bbox = gtk.VButtonBox()

    bbox.set_border_width(5)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)
    return bbox

frame=gtk.Frame('Ram 1')
box=mkBox()
frame.add(box)
frame1=gtk.Frame('Ram 2')
box1=mkBox(False,10,gtk.BUTTONBOX_SPREAD)
frame1.add(box1)

fc=gtk.FileChooser()

addBtn(box,'Indata','clicked',quit)
addBtn(box,'Quit','released',quit)
addBtn(box1,'Indata','clicked',quit)
addBtn(box1,'Quit','released',quit)
indata=gtk.Entry()
box.add(indata)
readdata=indata.get_text()

hbox=gtk.HBox()
hbox.set_border_width(20)

hbox.pack_start(frame)
hbox.add(frame1)
w=gtk.Window(gtk.WINDOW_TOPLEVEL)
w.add(hbox)
w.show_all()
gtk.main()
exit

