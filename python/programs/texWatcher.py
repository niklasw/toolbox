#!/usr/bin/python

import os,thread
from pyinotify import ThreadedINotify, EventsCodes, ProcessEvent

logSuffix='_texWatcher.log'
trunk=lambda s: os.path.splitext(s)[0]

def runLatex(sourceFile,pdf=''):
    exe=pdf+'latex'
    log=os.popen(exe+' '+sourceFile).read()
    open(trunk(sourceFile)+logSuffix,'w').write(log)

class PEaction(ProcessEvent):
    def __init__(self):
        ProcessEvent.__init__(self)

    def process_IN_MODIFY(self, event_k):
        file=os.path.join(event_k.path,event_k.name)
        thread.start_new_thread(runLatex,())

    def process_IN_CREATE(self, event_k):
        file=os.path.join(event_k.path,event_k.name)
        thread.start_new_thread(runLatex,())


