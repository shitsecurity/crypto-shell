#!/usr/bin/env python

from models import db

from lib.static import Static

class Sessions( Static, dict ): pass

class SQLiteHandler( object ):

	def __init__( self, *args, **kwargs ):
		session = Sessions.acquire()
		self.db = session.setdefault( db.SQLite.key, db.SQLite.create() )
		super( SQLiteHandler, self ).__init__( *args, **kwargs )

	def get_db( self ): return self.db
