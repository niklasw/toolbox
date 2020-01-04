#!/usr/bin/env python3

from tkinter import *

master = Tk()

w = Canvas(master, width=800, height=400)
w.pack()

w.create_line(0, 0, 800, 400)
w.create_line(0, 400, 800, 0, fill="red", dash=(14, 14))

w.create_rectangle(50, 25, 150, 75, fill="blue")

mainloop()
