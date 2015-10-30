#!/usr/bin/env python

import re
import string
import random

class Obfuscator(object):

    def __init__(self, shellcode=None):
        self.vars = {}
        self.pollutants = {}
        self.alphabet =string.letters + '_' + string.digits
        if shellcode is not None: self.shellcode = shellcode

    def var(self, id):
        return self.vars[ id ]

    def set(self, id):
        var = ''.join([random.choice(string.letters + '_')
                       for _ in xrange(random.randrange(6,13))])
        self.vars[id] = var
        return var

    def depollute(self, key):
        return self.pollutants[key]

    def pollute(self, payload, key=None):
        pollutant = ''.join([random.choice(self.alphabet)
                             for _ in xrange(random.randrange(2,6))])

        def to_toxic(chunk, pollutant):
            op = random.randrange(0,3)
            if op==0:
                return chunk + pollutant
            elif op==1:
                return pollutant + chunk
            elif op==2:
                return pollutant + chunk + pollutant

        toxic = ''.join([to_toxic(chunk,pollutant)
                         for chunk in self.chunkify(payload)])
        self.pollutants[key or payload] = pollutant
        return toxic

    def chunkify(self, str):
        current = 0
        strlen = len(str)-1
        while True:
            offset = random.randrange(1,6)
            yield str[current:current+offset]
            current += offset
            if current > strlen:
                break

    def add_comment(self, payload, type):
        if type=='php':
            comment_format = '{blank}/*{comment}*/'
        comment = ''.join([random.choice(string.letters + '_' + string.digits)
                           for _ in xrange(random.randrange(0,16))])
        blank = random.choice(['\n','\t','',' '])
        propogate = comment_format.format(blank=blank, comment=comment)
        return propogate + payload
