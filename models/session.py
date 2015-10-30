#!/usr/bin/env python

from db import Base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Unicode
from sqlalchemy.orm.exc import NoResultFound as NoResult

class Session(Base):

    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__ (self):
        return "<Session {}>".format(self.name)
