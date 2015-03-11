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
