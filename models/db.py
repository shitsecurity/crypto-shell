#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func as function
from sqlalchemy.orm import exc as exceptions

Base = declarative_base()

class DBSession( object ):

	@property
	@classmethod
	def key( cls ):
		return cls.__class__.__name__

class SQLite( DBSession ):

	@staticmethod
	def create():
		engine=create_engine('sqlite:///shell.db')
		Base.metadata.create_all(engine)
		return sessionmaker(bind=engine)()
