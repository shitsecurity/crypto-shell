#!/usr/bin/env python

from db import Base
from sqlalchemy import Column, UniqueConstraint
from sqlalchemy import Integer, String, Unicode, Boolean, Date
from datetime import datetime

class Shell( Base ):

	__tablename__ = 'shell'

	session = Column( String, nullable=False, index=True )

	id = Column( Integer, primary_key=True )
	file = Column( String )
	domain = Column( String, index=True )
	url = Column( String )
	key = Column( String, nullable=False )
	action = Column( String, nullable=False )
	comment = Column( String, default=None )
	alias = Column( String, index=True )
	shellcode = Column( String, nullable=False )

	active = Column( Boolean, default=True, index=True )
	created = Column( Date, default=datetime.now(), index=True )
	checked = Column( Date, default=datetime.now(), index=True )

	ip = Column( String, index=True )
	country = Column( String, index=True )

	pr = Column( Integer, index=True )
	tic = Column( Integer, index=True )

	UniqueConstraint( 'alias', 'session' )

	def __repr__ ( self ):
		return "<Shell {}>".format( self.domain )

	@property
	def uid( self ):
		return hex(self.id)
