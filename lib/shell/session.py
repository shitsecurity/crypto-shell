#!env/bin/python -i

from shell.handler import php
from shell.transport import query, Session as TransportSession
from shell.transport import xor_gzip_encoder, xor_gzip_decoder

from urlparse import urlparse

class Session( object ):

	def __init__( self, host, key, 	handler=php,
									action='PHPSESSID',
									encoder=xor_gzip_encoder,
									decoder=xor_gzip_decoder ):

		if not host.startswith('http'): host = 'http://{}'.format( host )
		self.domain = urlparse( host ).netloc

		self.session = TransportSession()
		self.transport_field = 'cookie'
		handle = lambda *args, **kwargs : handler( *args, **kwargs )
		self.q = lambda *args, **kwargs: query( host,
												handle( *args, **kwargs ),
												key,
												session=self.session,
												action=action,
												encoder=encoder,
												decoder=decoder,
												via=self.transport_field )

		self.last = None

	def __repr__( self ):
		return '<Session {}>'.format( self.domain )

	def __call__( self, *args, **kwargs ):
		self.last = self.q( *args, **kwargs )
		return self.last

	@property
	def user_agent( self ):
		return self.session.headers['user-agent']

	@user_agent.setter
	def user_agent( self, value ):
		self.session.headers['user-agent'] = value

	@property
	def field( self ):
		return self.transport_field

	@field.setter
	def field( self, value ):
		if value in ['cookie', 'post']:
			self.transport_field = value
		else:
			raise TypeError()
	
	@property
	def fields( self ):
		return ['cookie', 'post']

if __name__ == "__main__":

	import sys
	sys.ps1 = '$ '

	banner = '''
                 _______  ______ __   __  _____  _______  _____ 
                 |       |_____/   \_/   |_____]    |    |     |
                 |_____  |    \_    |    |          |    |_____|
                                                                
                      _______ _     _ _______              
                      |______ |_____| |______ |      |     
                      ______| |     | |______ |_____ |_____
	'''

	import code
	code.interact(local=locals(),banner=banner)
