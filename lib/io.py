#!/usr/bin/env python

import os.path

def get_name( file ):
    return os.path.splitext( file )[0]

def write_file( file, data ):
    with open( os.path.abspath( os.path.expanduser( file )), 'wb+' ) as fh:
        fh.write( data )

def read_file( file ):
    with open( os.path.abspath( os.path.expanduser( file )), 'rb' ) as fh:
        return ''.join(fh.readlines()).strip()

def escape( data, symbol='"' ):
    return data.replace(symbol,'\\{}'.format(symbol))

def get_script_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..',
                                        'data',
                                        'scripts'))

def load_script( name ):
    return read_file( os.path.join( get_script_dir(), '{}.sh'.format( name )))

def load_script_names():
    return map(get_name, os.listdir(get_script_dir()))

def get_eval_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..',
                                        'data',
                                        'eval'))

def load_eval( file ):
    return read_file( os.path.join( get_eval_dir(), file ))

def load_eval_names():
    return os.listdir(get_eval_dir())

def echo( data, escape="'"):
    return data.replace(escape,'{esc}\\{esc}{esc}'.format(esc=escape))
