#!/usr/bin/python
import os.path, random, string
def random_filename(chars=string.hexdigits, length=16, prefix='', suffix='', \
                    verify=True, attempts=10):
    for attempt in range(attempts):
        filename = ''.join([random.choice(chars) for i in range(length)])
        filename = prefix + filename + suffix
        if not verify or not os.path.exists(filename):
           return filename


if __name__ == '__main__':
    rname = random_filename(length=8, prefix='random_', suffix='.txt')
    print rname

