#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Borg:
    _state = {}
    def __init__(self):
        self.__dict__ = self._state

class A(Borg):
    def __init__(self,val=None):
        Borg.__init__(self)
        self.value = val

    def __str__(self):
        s = 'variables:\n'
        for key,val in self.__dict__.iteritems():
            s += '{0} = {1}\n'.format(key,val)
        return s


a = A()
print 'a',a

a = A(6)
print 'a',a

b = A()

print 'a',a
print 'b',b

a.whatever = 'Nice'

a.value = 123
print 'b',a
print 'b',b

b.holahoop = 'Fun'
print 'a',a

c = A()
print 'c',c


