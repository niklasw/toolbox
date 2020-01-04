#!/usr/bin/python

import sys,os
import fileinput

bufsize = 10000

def timer(func):
    import time
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper

@timer
def genFile():
    fileName = "/tmp/fastFileParser.txt"
    with open(fileName,'w') as fp:
        for i in range(int(1e6)):
            fp.write('{} hejsan\n'.format(i))
    return fileName


def lineOp(line,func):
    if line:
        return func(line.strip().split()[0])
    else:
        return func(0)

@timer
def bufread(filename):
	fh = open(filename,'r')
        output = 0
        number = 0
	while 1:
		buf = fh.read(bufsize)
		try:
			buf += fh.readline().rstrip()
		except:
			pass
		lines=buf.split('\n')
		for line in lines:
                        output += lineOp(line,int)
		if len(buf) < bufsize:
			break
        return output

@timer
def firead(filename):
        output = 0
	for line in fileinput.input(filename,bufsize=bufsize):
                output += lineOp(line,int)
        return output

@timer
def normalread(filename):
    output = 0
    with open(filename,'r') as fp:
        for line in fp:
            output += lineOp(line,int)
    return output


filename = genFile()
print(bufread(filename))
genFile()
print(firead(filename))
genFile()
print(normalread(filename))
