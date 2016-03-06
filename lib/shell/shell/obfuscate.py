#!/usr/bin/env python

import re
import string
import random

from misc import base64_encode

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

    def operation(self, op, spaces=None):
        randspace = lambda: spaces if spaces is not None and random.randrange(0,2) else ''
        return '{}{}{}'.format(randspace(), op, randspace())

    def quote(self, payload, quotes=None):
        if quotes is None:
            quote = random.choice(['\'','\"'])
        else:
            quote = quotes
        return '{}{}{}'.format(quote, payload, quote)

    def set_wrap(self, id, payload, key=None, encoder='b64', code='php'):
        var = self.set(id)
        if encoder == 'b64':
            payload = base64_encode(payload)
        chunks = list(self.chunkify(payload, bounds=(32,64)))
        result = ''
        if code == 'php':

            def concat(index):
                if ii == 0:
                    op = '='
                else:
                    op = '.='
                return op

            def linebreak(index, total):
                if ii == total-1:
                    ln = ''
                else:
                    ln = '\n'
                return ln

            for ii, chunk in enumerate(chunks):
                result += '${}{}{};{}'.format(var,
                                              self.operation(concat(ii), spaces=''),
                                              self.quote(chunk),
                                              linebreak(ii,len(chunks)))
        return result

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

    def chunkify(self, str, bounds=(1,6)):
        current = 0
        strlen = len(str)-1
        while True:
            offset = random.randrange(*bounds)
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
