#!/usr/bin/env python3

class A():
    value = 1

    def __init__(self):
        print(self.value)


class B(A):
    value = 2

    def __init__(self):
        super().__init__()


class D():
    value = 3

    def __init__(self):
        self.other = globals()['B']
        print(self.other.value)
