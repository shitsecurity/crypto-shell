#!/usr/bin/env python

import os
import sys
import shlex

from cli import color
from modules.module import Module
from lib.shell.session import Session, cmds as hello

from collections import OrderedDict

class Connect( Module ):

	__module__ = 'transport.web'

	options = OrderedDict()

	options['dir'] = '~'
	options['user-agent'] = 'Mozilla/5.0'
	
	_prompt_ = '{blue}.::{cyan}{domain}{purple}@{cyan}{ip}' \
				'{blue}::{cyan}{path}' \
				'{blue}::{purple}${white} '

	def __init__( self, shell, *args, **kwargs ):
		super( Connect, self ).__init__( *args, **kwargs )
		self.set_prompt(domain=shell.domain, ip=shell.ip,
						path=self.env.get('dir','~') )
		self.transport = Session( shell.url, shell.key, action=shell.action )
		self.transport.user_agent = self.env.get('user-agent','Mozilla/5.0')
		print self.transport(hello)

	def default( self, line ):
		if line.strip()=='':
			return
		cmds = []
		if self.env.get('dir','~')!='~':
			cmds.append('cd {}'.format( self.env['dir'] ))
		cmds.append(line)
		print '{}{}{}'.format(color.GREEN, self.transport(cmds), color.NORMAL)

	def onecmd( self, line ):
		if line.startswith('@'):
			return super( Connect, self ).onecmd( line.lstrip('@') )
		elif line.strip()=='EOF':
			sys.exit()
		else:
			return self.default( line )

	def completenames(self, text, *ignored):
		dotext = 'do_'+text
		return ['@'+a[3:] for a in self.get_names() if a.startswith(dotext)]

	def complete(self, text, *args, **kwargs ):
		return super(Connect,self).complete(text.lstrip('@'),*args,**kwargs)

	def completedefault( self, text, line, b_index, e_index ):
		args = shlex.split(line)
		return getattr(self, 'complete_' + args[0].lstrip('@'))( text, line, b_index, e_index )

	def help_cd( self ):
		print ' Usage: cd [dir]'

	def do_cd( self, line ):
		'''change working directory'''
		args = shlex.split(line)
		if len(args)>1:
			self.help_cd()
			return
		dir = args[0] if len(args)==1 else '~'
		if dir=='~':
			path = '~'
		else:
			path = os.path.abspath( os.path.join( self.get_path(), dir ))
		self.env['dir'] = path
		self.set_prompt(path=path)

	# XXX @download
	# XXX @upload
	# XXX @script
