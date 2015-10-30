#!/usr/bin/env python

from db import Base
from sqlalchemy import Column, UniqueConstraint
from sqlalchemy import Integer, String, Unicode, Boolean, Date
from datetime import datetime

from sqlalchemy.orm import validates

import os

from lib.shell.generate import list_handlers

class Shell(Base):

    __tablename__ = 'shell'

    session = Column(String, nullable=False, index=True)

    id = Column(Integer, primary_key=True)
    file = Column(String)
    domain = Column(String, index=True)
    url = Column(String)
    key = Column(String, nullable=False)
    password = Column(String, nullable=False)
    action = Column(String, nullable=False)
    comment = Column(String, default=None)
    alias = Column(String, index=True)
    shellcode = Column(String, nullable=False)

    active = Column(Boolean, default=True, index=True)
    created = Column(Date, default=datetime.now(), index=True)
    checked = Column(Date, default=datetime.now(), index=True)

    ip = Column(String, index=True)
    country = Column(String, index=True)

    pr = Column(Integer, index=True)
    tic = Column(Integer, index=True)

    UniqueConstraint('alias', 'session')

    handler = Column(String, index=True, default='php')

    @validates('handler')
    def validate_handler(self, key, handler):
        if handler not in list_handlers():
            raise ValueError(handler)
        return handler

    def __repr__ (self):
        return "<Shell {}>".format(self.domain)

    @property
    def uid(self):
        return hex(self.id)
