#!/usr/bin/env python

class Static( object ):
	
	__instance__ = None

	@classmethod
	def acquire( cls, *args, **kwargs ):
		if cls.__instance__ is None:
			cls.__instance__ = cls( *args, **kwargs )
		return cls.__instance__
