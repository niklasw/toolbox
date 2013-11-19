#!/usr/bin/env python

import os,sys
from getpass import *

USER     = os.getenv('USER')
PASSWORD = getpass('Enter password for proxy: ')

os.environ['http_proxy'] = 'http://%s:%s@PROXYSESO1.SCANIA.COM:8080' % (USER,PASSWORD)


