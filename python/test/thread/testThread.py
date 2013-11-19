#!/usr/bin/python

import os,sys,thread,time

def f(arg=''):
    global pidlist
    pidlist.append(os.getpid())
    if arg=='kill':
        time.sleep(1)
        print "Thread",thread.get_ident(),"is killed"
        sys.exit()
    while True:
        time.sleep(3)
        print "Thread",thread.get_ident(),"is alive"

pidlist=[os.getpid()]
thread.start_new_thread(f,())
thread.start_new_thread(f,())
thread.start_new_thread(f,('kill',))
print pidlist
while True:
    answer = raw_input("Stop thread now? Y/N: ")
    if answer in [ "Y", "y" ]:
        print "Exiting"
        break

sys.exit(0)
