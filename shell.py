#!/usr/bin/env python
# -*- coding: utf-8

'''
@shitsecurity
'''

import lib.thread

import os
import shlex
import socket
import getpass
import logging

from lib import log
from cli import cli, color
from models import db
from modules import module
from handlers.handler import Sessions
from handlers.session import SessionHandler, NonExistentSession

from straight.plugin import load

class Shell( cli.Cli ):

    __VERSION__ = '0.2'

    def __init__( self ):
        self.intro = '''{green}
         _______  ______ __   __  _____  _______  _____
         |       |_____/   \_/   |_____]    |    |     |
         |_____  |    \_    |    |          |    |_____|

              _______ _     _ _______
              |______ |_____| |______ |      |
              ______| |     | |______ |_____ |_____


                          version {}{normal}
        '''.format( '{}.{}' .format( color.CYAN, color.GREEN ) \
                    .join( self.__VERSION__.split('.')),
                    cyan = color.CYAN,
                    green = color.GREEN,
                    normal = color.NORMAL )

        default_session = 'default'
        self.set_prompt(getpass.getuser(),
                        socket.gethostname(),
                        os.getcwd(),
                        module='~',
                        session=default_session)
        cli.Cli.__init__( self )
        self.modules=dict([ ( _.__module__, _ )
                            for _ in load('modules', subclasses=module.Module)
                            if not _.__module__.startswith('.') ])
        self.handler = SessionHandler()
        self.handler.fetch_session( name=default_session )

    @classmethod
    def spawn( cls ): cls().run()

    def run( self ):
        try:
            self.cmdloop()
        except (SystemExit,KeyboardInterrupt):
            print '\n\n {}Hack the planet!{}\n'.format(color.GREEN,color.NORMAL)

    def do_modules( self, line ):
        '''show modules'''
        args = shlex.split( line )
        if args:
            self.help_modules()
            return
        pretty = self.pprint()
        for module in self.modules.values():
            print pretty.format(module.__module__)
        if len(self.modules) == 0:
            print self.pprint(marker='!').format('No loaded modules')

    def help_modules( self ):
        print ' Usage: modules'

    def do_sessions( self, line ):
        '''show sessions'''
        args = shlex.split(line)
        if args:
            self.help_sessions()
            return
        pretty = self.pprint()
        for session in self.handler.read_session_names():
            print pretty.format(session)

    def help_sessions( self ):
        print ' Usage: sessions'

    def do_load( self, line ):
        '''load session'''
        args = shlex.split(line)
        session = args[0] if( len(args)==1 ) else None
        if not session:
            self.help_load()
            return
        self.handler.fetch_session( name=session )
        self.set_prompt( session=session )

    def complete_load( self, text, line, b_index, e_index ):
        return self.default_complete(text,line,self.handler.read_session_names)

    def help_load( self ):
        print ' Usage: load [session]'

    def do_delete( self, line ):
        '''delete session'''
        args = shlex.split(line)
        session = args[0] if( len(args)==1 ) else None
        if not session:
            self.help_delete()
            return
        try:
            self.handler.delete_session( name=session )
            if( self.handler.count_sessions() == 0 ):
                self.handler.create_session( name=session )
        except NonExistentSession:
            msg = 'Session {} not found'.format( session )
            print self.pprint(marker='!').format( msg )

    def help_delete( self ):
        print ' Usage: delete [session]'

    def complete_delete(self, text, line, b_index, e_index ):
        return self.default_complete(text,line,self.handler.read_session_names)

    def do_use( self, line ):
        '''use module'''
        args = shlex.split(line)
        module = args[0] if( len(args)==1 ) else None
        if not module:
            self.help_use()
            return
        if module not in self.modules.keys():
            msg = 'Module {} not loaded'.format( module )
            print self.pprint(marker='!').format( msg )
            return
        self.set_prompt( module=module )
        self.modules[ self.get_module() ].spawn( self )
        self.set_prompt( module='~' )

    def help_use( self ):
        print ' Usage: use [module]'

    def complete_use( self, text, line, b_index, e_index ):
        return self.default_complete(text,line,self.modules.keys)

    def do_logging( self, line ):
        '''toggle logging'''
        args = shlex.split(line)
        action = args[0] if len(args)==1 else None
        if not action:
            self.help_logging()
            return
        if action.lower()=='on':
            log.log(level=logging.DEBUG,filename='shell.log')
        elif action.lower()=='off':
            log.log(level=logging.NOTSET,filename='shell.log')
        else:
            msg = 'Argument {} invalid'.format( action )
            print self.pprint(marker='!').format( msg )

    def help_logging( self ):
        print ' Usage: logging [on|off]'

    def complete_logging( self, text, line, b_index, e_index ):
        return self.default_complete(text, line, lambda: ['on','off'])

if __name__ == "__main__":
    Shell.spawn()
