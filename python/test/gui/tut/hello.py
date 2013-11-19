#!/usr/bin/python

import gtk,sys

def hello(b,msg):
    print b
    print "Hello, World!",msg.get_text()

def quit(b):
    sys.exit(0)


class myBut(gtk.Button):
    def __init__(self,bText="Press my but", ent=''):
        gtk.Button.__init__(self,bText)
        self.connect('clicked',self.event)
        self.ent = ent
        self.result=''

    def tip(self,toolTip='Tip'):
        self.set_tooltip_text(toolTip)

    def event(self,b):
        if self.ent:
            print self.ent.get_text()


def createBbox(horizontal=True, title=None, spacing=0,layout=gtk.BUTTONBOX_SPREAD):
    frame = gtk.Frame(title)

    if horizontal:
        bbox = gtk.HButtonBox()
    else:
        bbox = gtk.VButtonBox()
    frame.add(bbox)

    bbox.set_border_width(5)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)


    entry = gtk.Entry()
    bbox.add(entry)
    entry.insert_text('Skriv na')

    text =  entry.get_text()
    print text

    button = gtk.Button("Press me")
    button.connect('clicked',hello,entry)
    button.set_tooltip_text("Press this and live on")
    bbox.add(button)

    myButton = myBut(ent=entry)
    myButton.tip('Heja heja')

    button = gtk.Button("Quit")
    button.connect('released',quit)
    bbox.add(button)
    bbox.add(myButton)

    return frame

hbox=gtk.VBox()
hbox.set_border_width(10)
hbox.pack_start(createBbox(False, "Spread", 40, gtk.BUTTONBOX_SPREAD))
w=gtk.Window(gtk.WINDOW_TOPLEVEL)
w.add(hbox)
w.show_all()
gtk.main()
exit

