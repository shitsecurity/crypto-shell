#!/usr/bin/python
# -*- coding: utf-8

import readline
import sys
import cmd
import traceback
import shlex

import color
import pprint

class Cli(cmd.Cmd, pprint.PPrint):

    _prompt_ = '{blue}.::{cyan}{session}'\
                '{blue}::{cyan}{module}'\
                '{blue}::{purple}${white} '

    help = []

    def resolve_ip(self): return None

    def get_module(self):
        return self.module

    def get_path(self):
        return self.path

    def get_session(self):
        return self.session

    def set_prompt(self,
                   user=None,
                   domain=None,
                   path=None,
                   module=None,
                   session=None,
                   ip=None):

        if user is not None:
            self.user = user
        if domain is not None:
            self.domain = domain
        if path is not None:
            self.path = path
        if module is not None:
            self.module = module
        if session is not None:
            self.session = session

        ipaddr = ip or self.resolve_ip() or '127.0.0.1'

        self.prompt = self._prompt_.format(blue=color.BLUE,
                                           cyan=color.CYAN,
                                           purple=color.PURPLE,
                                           white=color.WHITE,
                                           path=self.path,
                                           user=self.user,
                                           domain=self.domain,
                                           module=self.module,
                                           session=self.session,
                                           ip=ipaddr)

    def __init__(self):
        self.doc_header = ' Commands (type [help|?] [command]):'
        self.doc_leader = self.doc_header
        self.ruler = '-'
        self.undoc_header = None
        self.misc_header = None
        self.nohelp = ' No help for command: %s'
        self.identchars = self.identchars + ':'
        delims = readline.get_completer_delims()
        readline.set_completer_delims(delims.replace(':','')\
                                            .replace('/','')\
                                            .replace('-','')\
                                            .replace('_','')\
                                            .replace('@',''))
        cmd.Cmd.__init__(self)

    def do_help(self, line):
        '''show this message'''
        cmd.Cmd.do_help(self, line)

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if header != self.doc_header:
            return
        print ' '+self.ruler*(len(self.doc_header)-1)
        for cmd in cmds:
            doc = getattr(self, 'do_'+cmd).__doc__
            print ' {} {}'.format(cmd.ljust(15), doc)

    def emptyline(self):
        pass

    def default(self, line):
        print ' {}Invalid command{}'.format(color.GREEN, color.NORMAL)

    def colorify(self): sys.stdout.write(color.GREEN)

    def pipe(self, line):
        lines = line.split('|')
        xargs = []
        result = None
        try:
            for ii,line in enumerate(lines):
                args = line.strip().split(' ',1)
                action = args[0]
                line = args[1] if len(args)==2 else ''
                if ii: xargs = [result,]
                result = getattr(self, 'do_'+action)(line,*xargs)
        except AttributeError:
            self.default(line)

    def is_piped(self, line):
        return '|' in line

    def onecmd(self, line):
        self.colorify()
        try:
            if self.is_piped(line):
                self.pipe(line)
            else:
                return cmd.Cmd.onecmd(self, line)
        except SystemExit:
            raise
        except:
            msg = traceback.format_exc().rstrip()
            print '{}{}{}'.format(color.RED, msg, color.NORMAL)

    def do_EOF(self, line):
        sys.exit()

    def default_complete(self, text, line, f):
        args = shlex.split(line)
        if len(args)==1:
            complete = ''
        elif len(args)==2 and text.strip()!='':
            complete = text
        else:
            complete = None
        if complete is not None:
            return [_ for _ in map(str,f()) if _.startswith(complete)]

class InteractiveMixin(object):

    def default(self, line):
        if line.strip()=='':
            return
        result = self.default_action(line)
        if result:
            print '{}{}{}'.format(color.GREEN, result, color.NORMAL)

    def onecmd(self, line):
        if line.startswith('@'):
            return super(InteractiveMixin, self).onecmd(line.lstrip('@'))
        elif line.strip()=='EOF':
            sys.exit()
        else:
            self.default(line)

    def completenames(self, text, *ignored):
        dotext = 'do_'+text
        return ['@'+a[3:] for a in self.get_names() if a.startswith(dotext)]

    def complete(self, text, *args, **kwargs):
        line = readline.get_line_buffer().strip()
        if line.startswith('@') or line.strip()=='':
            return super(InteractiveMixin, self).complete(text.strip('@'), *args, **kwargs)

    def completedefault(self, text, line, b_index, e_index):
        args = shlex.split(line)
        return getattr(self, 'complete_'+args[0].lstrip('@'))(text, line, b_index, e_index)
