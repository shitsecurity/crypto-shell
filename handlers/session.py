#!/usr/bin/env python

from handler import SQLiteHandler
from models.session import Session, NoResult

class NonExistentSession( Exception ): pass

class SessionHandler( SQLiteHandler ):

    def fetch_session( self, name ):
        try:
            return self.db.query(Session).filter_by(name=name).one()
        except NoResult:
            return self.create_session( name )

    def create_session( self, name ):
        session = Session(name=name)
        self.db.add( session )
        self.db.commit()
        return session

    def read_session_names( self ):
        return [ _[0] for _ in self.db.query(Session.name).distinct().all() ]

    def read_session( self, name ):
        try:
            return self.db.query(Session).filter_by(name=name).one()
        except NoResult:
            raise NonExistentSession()

    def count_sessions( self ):
        return self.db.query(Session.name).distinct().count()

    def delete_session( self, name ):
        if( not self.db.query(Session).filter_by(name=name).delete() ):
            raise NonExistentSession()
        self.db.commit()
