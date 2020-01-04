#!/usr/bin/env python3

import graphics as g
import time

def flashCircle(window, c=g.Point(0,0),r=100):
    circle = g.Circle(c,r)
    circle.setFill('black')
    circle.draw(window)
    time.sleep(1)
    circle.setFill('blue')
    time.sleep(1)
    circle.undraw()
    return circle


def main():
    win = g.GraphWin('My win', 500,300)
    win.setBackground('red')

    flashCircle(win, g.Point(100,100), 100)
    flashCircle(win, g.Point(200,100), 50)

    time.sleep(1)
    #win.getMouse()
    win.close()

main()
