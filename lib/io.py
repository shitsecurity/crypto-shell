#!/usr/bin/env python

import os.path

def write_file( file, data ):
	with open( os.path.abspath( os.path.expanduser( file )), 'wb+' ) as fh:
		fh.write( data )

def read_file( file ):
	with open( os.path.abspath( os.path.expanduser( file )), 'rb' ) as fh:
		return ''.join(fh.readlines())

def escape( data, symbol='"' ): 
	return data.replace('\\','\\\\').replace(symbol,'\\{}'.format(symbol))

def get_script_dir():
	return os.path.abspath(os.path.join(os.path.dirname(__file__),
										'..',
										'data',
										'scripts'))

def load_script( name ):
	return read_file( os.path.join( get_script_dir(), '{}.sh'.format( name )))

def load_script_names():
	return [ os.path.splitext(_)[0] for _ in os.listdir(get_script_dir()) ]
