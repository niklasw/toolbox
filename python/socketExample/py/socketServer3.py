#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketserver
import os
from os.path import join as pjoin

class conf:
    tag = '-<O>='
    port = 9999
    buff = 1024
    encoding = 'utf-8'
    host = 'localhost'
    targetDir = '/tmp/tcpFiles'
    fileName = ''

    def __init__(self):
        pass

class MyTCPHandler(socketserver.BaseRequestHandler):

    def getFileName(self):
        if not conf.fileName:
            data = self.request.recv(conf.buff)
            self.request.sendall(data)
            check = self.request.recv(10).decode()
            if check == 'OK':
                print('Got file name',data.decode(),'.')
                conf.fileName = data.decode()
            else:
                print('File name check not OK')
                conf.fileName = ''


    def getFile(self):
        enc = conf.encoding
        tag = conf.tag
        if not conf.fileName:
            print('Error. No filename.')
            return

        targetFile = pjoin(conf.targetDir,conf.fileName)
        with open(targetFile, 'wb') as fp:
            while True:
                data = self.request.recv(conf.buff)
                print('... {} bytes for {}\n'.format(len(data),conf.fileName))
                if not data:
                    break
                fp.write(data)
        conf.fileName = ''

    def handle(self):
        self.getFileName()
        if conf.fileName:
            self.getFile()

class fileReciever:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        pass

    def runServer(self):
        HOST, PORT = self.host, self.port
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            print('Starting server')
            server.serve_forever()

if __name__ == "__main__":
    server = fileReciever(conf.host,conf.port)
    server.runServer()

