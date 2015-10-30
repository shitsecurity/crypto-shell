#!/usr/bin/env python

class mdict(dict):

    def __init__(self, kwargs=None):
        if kwargs is None: return
        for k,v in kwargs:
            self.__setitem__(k, v)

    def __setitem__(self, key, value):
        self.setdefault(key, []).append(value)
