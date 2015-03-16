#!/usr/bin/env python

import os
import sys
import shlex

from cli import color
from cli.cli import InteractiveMixin
from modules.module import Module
from lib.process import call
from lib.io import write_file, read_file, escape, load_script, load_script_names
from lib.shell.session import Session, cmds as hello

from tempfile import NamedTemporaryFile
from collections import OrderedDict

class Connect( InteractiveMixin, Module ):

	__module__ = 'transport.web'

	options = OrderedDict()

	options['dir'] = '~'
	options['editor'] = 'vim'
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

	def hello( self ):
		return self.execute(hello)

	def execute( self, cmds ):
		return self.transport( filter( None, cmds ))

	def cwd( self ):
		if self.env.get('dir','~')!='~':
			return 'cd {}'.format( self.env['dir'] )

	def execute_one( self, cmd ):
		return self.execute([ self.cwd(), cmd ])

	def default_action( self, line ):
		return self.execute_one( line )

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

	def help_download( self ):
		print ' Usage: download [remote] [local]'

	def do_download( self, line ):
		'''download file'''
		args = shlex.split( line )
		if len(args) not in [1,2]:
			self.help_download()
			return
		remote = args[0]
		local = args[1] if len(args)==2 else os.path.basename(remote)
		write_file(local,self.execute_one('cat {}'.format(remote)))

	def help_upload( self ):
		print ' Usage: upload [local] [remote]'

	def do_upload( self, line ):
		'''upload file'''
		args = shlex.split( line )
		'''upload file'''
		if len(args) not in [1,2]:
			self.help_download()
			return
		local = args[0]
		remote = args[1] if len(args)==2 else os.path.basename(local)
		self.execute_one('echo "{}" > {}'.format(escape(read_file(local)),remote))

	def help_edit( self ):
		print ' Usage: edit [file]'

	def do_edit( self, line ):
		'''edit file'''
		args = shlex.split(line)
		file = args[0] if len(args)==1 else None
		if not file:
			self.help_edit()
			return
		original = self.execute_one('cat {}'.format(file))
		tmpfile = NamedTemporaryFile(suffix=os.path.splitext(file)[1])
		write_file( tmpfile.name, original )
		os.system('{} {}'.format( self.env['editor'], tmpfile.name ))
		mod = read_file( tmpfile.name )
		tmpfile.close()
		if original!=mod:
			self.execute_one('echo "{}" > {}'.format(escape(mod),file))

	def help_script( self ):
		print ' Usage: script [name] [outfile]'

	def do_script( self, line ):
		'''execute script'''
		args = shlex.split( line )
		if len(args) not in [1,2]:
			self.help_script()
			return
		name = args[0]
		outfile = args[1] if len(args)==2 else None
		try:
			script = load_script(name)
		except IOError:
			msg = 'Invalid script name {}'.format( name )
			print self.pprint(marker='!').format( msg )
			return
		cmds = [ self.cwd(), ] + self.script_to_cmds(script)
		output = self.execute(cmds)
		if outfile:
			write_file(outfile,output)
		print output

	def script_to_cmds( self, script ):
		return filter( lambda _: _ and not _.strip().startswith('#'),
						script.split('\n'))

	def complete_script( self, text, line, b_index, e_index ):
		return self.default_complete( text, line, load_script_names )
