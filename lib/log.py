#!/usr/bin/env python

import logging

def log( level=logging.INFO, filename=None ):
	logging.basicConfig(level=level, filename=filename,
						format='[%(asctime)s %(levelname)s] %(message)s',
						datefmt='%m/%d/%Y %I:%M:%S' )
	requests_logger = logging.getLogger("requests")
	requests_logger.setLevel( logging.WARNING )
