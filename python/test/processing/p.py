#!/usr/bin/python
from processing import Process, Queue
import time

def f(i):
    while 1:
        i+=1
        time.sleep(1)
        print i

if __name__ == '__main__':
    for i in range(10):
        p = Process(target=f, args=[i])
        p.start()


