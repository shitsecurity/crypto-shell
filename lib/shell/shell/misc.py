#!/usr/bin/env python

def base64_encode(payload):
    return str(payload).encode('base64').replace('\n','')
