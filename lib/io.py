#!/usr/bin/env python

import os.path

def write_file( file, data ):
	with open( os.path.expanduser( file ), 'wb+' ) as fh:
		fh.write( data )
