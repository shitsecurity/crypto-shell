#!/usr/bin/env python

import logging
import traceback

from handler import SQLiteHandler
from models.db import function as f, exceptions
from models.shell import Shell

from cli.pprint import PPrint

from geoip import geolite2
from socket import gethostbyname
from iptools import IpRange
from urlparse import urlparse
from datetime import datetime

from lib.seo.pr import pr as page_rank
from lib.seo.tic import tic as tic_rank

class LocalIP( Exception ): pass

class ShellHandler( SQLiteHandler, PPrint ):

	def __init__( self, session, *args, **kwargs ):
		super( ShellHandler, self ).__init__( *args, **kwargs )
		self.session = session

	def save( self, shell ):
		shell.session = self.session
		self.db.add(shell)
		self.db.flush()
		self.db.refresh(shell)
		self.db.commit()

	def in_session(self,query): return query.filter(Shell.session==self.session)

	def get_uniq( self ):
		query = self.db.query(f.coalesce( Shell.alias, Shell.id ))
		return [ _[0] for _ in self.in_session( query ).all() ]

	def _get_shells( self, id=None, alias=None ):
		query = self.db.query( Shell )
		if id is not None: query = query.filter( Shell.id==id )
		if alias is not None: query = query.filter( Shell.alias==alias )
		return self.in_session( query )

	def get_shell( self, *args, **kwargs ):
		return self._get_shells( *args, **kwargs ).one()

	def delete_shell( self, *args, **kwargs ):
		result = self._get_shells( *args, **kwargs ).delete()
		self.db.commit()
		return result

	def get_shell_by_uniq( self, param ):
		if param.startswith('@'):
			return self.get_shell( alias=param )
		try:
			return self.get_shell( id=int(param) )
		except ValueError:
			raise NoResult()

	def delete_shell_by_uniq( self, param ):
		if param.startswith('@'):
			return self.delete_shell( alias=param )
		try:
			return self.delete_shell( id=int(param) )
		except ValueError:
			return False

	def update_alias( self, shell, alias ):
		if not alias.startswith('@'): alias = '@'+alias
		shell.alias = alias
		self.db.commit()

	def delete_alias( self, shell ):
		shell.alias = None
		self.db.commit()

	def update_url( self, shell, url ): # XXX
		if not url.startswith('http'): url = 'http://' + url
		shell.url = url
		domain = urlparse( url ).netloc
		shell.domain = domain

		try:
			ip = gethostbyname(domain)
			shell.ip = ip

			if ip in IpRange('127.0.0.1/8'):
				raise LocalIP()

			shell.country = geolite2.lookup(ip).country

			try:
				shell.tic = tic_rank( domain )
			except:
				shell.tic = None
				msg = 'Failed to fetch tic for {}'.format( domain )
				print self.pprint(marker='!').format( msg )
				logging.debug(traceback.format_exc())

			try:
				shell.pr = page_rank( domain )
			except:
				shell.pr = None
				msg = 'Failed to fetch page rank for {}'.format( domain )
				print self.pprint(marker='!').format( msg )
				logging.debug(traceback.format_exc())

		except LocalIP: pass

		except:
			shell.ip = None
			shell.country = None
			msg = 'Failed to resolve {}'.format( domain )
			print self.pprint(marker='!').format( msg )

		self.db.commit()

	def update_comment( self, shell, comment ):
		shell.comment = comment
		self.db.commit()

	def count_shells( self ):
		return self._get_shells().count()

	def count_vhosts( self ):
		return self._get_shells().group_by(Shell.domain).count()

	def get_alias( self ):
		return [ _[0] for _ in self.db.query( Shell.alias ).distinct().all() ]

	def update_checked( self, shell ):
		shell.checked = datetime.now()
		self.db.commit()
