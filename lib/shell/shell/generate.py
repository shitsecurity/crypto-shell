#!/usr/bin/env python

from misc import base64_encode
from hashlib import sha1
from jinja2 import Environment, PackageLoader, FileSystemLoader

import os

def key( strength=16 ):
    return os.urandom(strength).encode('hex')

def template_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..',
                                        'templates'))

def shell_path():
    return os.path.join( template_path(), 'shells' )

def cryptor_path():
    return os.path.join( template_path(), 'cryptors' )

def generate( file, path, key='', action='PHPSESSID', obfuscate=None ):
    env = Environment( loader=FileSystemLoader( path ))
    env.filters['base64'] = base64_encode
    return env.get_template( file ).render( key=key,
                                            obfs=obfuscate,
                                            action=action )

def generate_shell( *args, **kwargs ):
    return generate( *args, path=shell_path(), **kwargs )

def generate_cryptor( *args, **kwargs ):
    return generate( *args, path=cryptor_path(), **kwargs )

def minify( payload ):
    return payload.replace('\n','').replace('\t','').replace('    ','')

def remove_tags( payload, open, close ):
    return payload.replace(open,'',1)[::-1].replace(close[::-1],'',1)[::-1]

def remove_tags_php( payload ):
    return remove_tags( payload, open='<?php ', close='?>' )

def list_shells():
    return os.listdir(shell_path())

def list_cryptors():
    return os.listdir(cryptor_path())
