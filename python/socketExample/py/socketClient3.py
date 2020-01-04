#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import sys
from socketServer3 import conf

enc = conf.encoding

sendFiles = sys.argv[1:]


# Create a socket (SOCK_STREAM means a TCP socket)

def sendFileName(fileName,HOST,PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(fileName.encode())
        rFileName = sock.recv(conf.buff).decode().strip()
        if rFileName == fileName:
            sock.sendall('OK'.encode())
            return True
    return False


def sendFile(fileName, HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        with open(fileName,'rb') as fp:
            while True:
                data = fp.read(conf.buff)
                if not data:
                    break
                sock.sendall(data)
                print('read {} bytes from {}'.format(len(data),f))


if __name__ == '__main__':
    HOST, PORT = conf.host, conf.port
    for f in sendFiles:
        check = sendFileName(f,HOST,PORT)
        if check:
            sendFile(f,HOST,PORT)

    # Receive data from the server and shut down
    #print("Received: {}".format(received.strip()))
