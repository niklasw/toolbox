#!/usr/bin/python
# from http://www.btessentials.com/examples/examples.html
from bluetooth import *

server_address = "00:21:FE:C0:8E:28"
port = 1

sock = BluetoothSocket( RFCOMM )
sock.connect((server_address, port))

sock.send("hello!!")

sock.close()
