#!/usr/bin/env python3

import os
import sys
import time
from datetime import datetime


def file_action(filename: str):
    print(f'Do it with {filename}')


def file_check(filename: str, last_change: datetime):
    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
    if mtime > last_change:
        file_action(filename)
        return mtime
    return last_change


try:
    file_path = sys.argv[1]
except Exception:
    print('Needs file path argument')
    sys.exit(1)


mtime = datetime.fromtimestamp(0)

while True:
    if os.path.exists(file_path):
        mtime = file_check(file_path, mtime)
    else:
        print(f'no file {file_path}')
    time.sleep(1)
