#!/usr/bin/env python

import os
import copy
import shlex
import functools

import socket
import getpass

from cli.cli import Cli

from collections import OrderedDict

def require( key ):
	def decorator( f ):
		@functools.wraps( f )
		def decoree( self, *args, **kwargs ):
			if self.env[key] is None:
				msg = 'Required option {} not set.'.format(key)
				print self.pprint(marker='!').format(msg)
			else:
				return f( self, *args, **kwargs )
		return decoree
	return decorator

class Module( Cli ):

	options = OrderedDict()

	required = []

	@classmethod
	def run( cls, *args, **kwargs ):
		try:
			cls( *args, **kwargs ).cmdloop()
		except (SystemExit,KeyboardInterrupt):
			print ''

	def __init__( self, shell ):
		Cli.__init__( self )
		self.env = copy.copy( self.options )
		self.set_prompt(getpass.getuser(),
						socket.gethostname(),
						os.getcwd(),
						module=self.__module__,
						session=shell.get_session())

	def do_set( self, line ):
		'''set variable'''
		args = shlex.split(line)
		key,value = (args[0],args[1]) if( len(args)==2 ) else (None,None)
		if not key or not value:
			self.help_set()
			return
		try:
			hook = getattr(self, 'set_'+key)
			value = hook( value )
		except AttributeError: pass
		self.env[ key ] = value

	def _complete_env( self, text, line ):
		args = shlex.split(line)
		if len(args)==1:
			complete = ''
			completions = self.env.keys()
		elif len(args)==2 and text.strip()!='':
			complete = text
			completions = self.env.keys()
		elif len(args)==2 and text.strip()=='' or len(args)>2: # set_complete_*
			complete = text
			optc = len(args)-3
			if text.strip()=='': optc+=1
			try:
				completions = getattr(self,'option_complete_'+args[1])(optc)or[]
			except AttributeError:
				complete = None
		else:
			complete = None
		if complete is not None:
			return [ _ for _ in completions if _.startswith(complete) ]
	
	def complete_set( self, text, line, b_index, e_index ):
		return self._complete_env( text, line )

	def help_set( self ):
		print ' Usage: set [key] [value]'

	def do_unset( self, line ):
		'''unset variable'''
		args = shlex.split(line)
		key = args[0] if( len(args)==1 ) else None
		if not key:
			self.help_unset()
			return
		try:
			if key in self.options:
				self.env[key]=self.options[key]
			else:
				del self.env[key]
		except KeyError:
			print ' Option {} not set.'.format( key )

	def help_unset( self ):
		print ' Usage: unset [key]'

	def complete_unset( self, text, line, b_index, e_index ):
		return self._complete_env( text, line )

	def do_reset( self, line='' ):
		'''reset options'''
		args = shlex.split(line)
		if len(args)>0:
			self.help_reset()
			return
		self.env = copy.copy( self.options )

	def help_reset( self ):
		print ' Usage: reset'

	def do_options( self, line ):
		'''show options'''
		args = shlex.split(line)
		if len(args)>0:
			self.help_options()
			return
		if len( self.env )==0:
			print self.pprint(marker='!').format('No options')
			return
		offset = max([ len(_) for _ in self.env.iterkeys() ])
		for key,value in self.env.iteritems():
			if key in self.required and self.env[key] is None:
				marker='!'
			else:
				marker='*'
			print self.aprint(align=offset,marker=marker).format(key,value)

	def help_options( self ):
		print ' Usage: options'
