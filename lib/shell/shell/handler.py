#!/usr/bin/env python

def php_exec( cmd ):
	if cmd == 'ip':
		return "echo {$_SERVER['REMOTE_ADDR']}"

	elif cmd == 'domain':
		return "echo {$_SERVER['SERVER_NAME']}"

	elif cmd == 'whoami':
		return "echo \".posix_getpwuid(posix_geteuid())['name'].\";echo \".posix_getpwuid(posix_getegid())['name'].\""

	elif cmd == 'cwd':
		return "echo \".getcwd().\""

	return cmd.replace('\\','\\\\').replace('"','\\\"').replace('$','\\$')

def php_system( cmd ):
	return 'system("{}");'.format( cmd )

def cmd_chain( language, iter ):
	return language(';'.join( iter )+';')

def php( cmds ):
	return cmd_chain(php_system, map(php_exec,cmds))
