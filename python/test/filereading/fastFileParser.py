#!/usr/bin/python

import sys,os

bufsize = 100000


def bufread(filename):
	fh = open(filename,'r')
	count = 0
	while 1:
		buf = fh.read(bufsize)
		try:
			buf += fh.readline().rstrip()
		except:
			pass
		lines=buf.split('\n')
		for line in lines:
			line.strip()
		if len(buf) < bufsize:
			break

def firead(filename):
	import fileinput
	for line in fileinput.input(filename,0,''):
		line.strip()



filename = sys.argv[1]

bufread(filename)
#firead(filename)
