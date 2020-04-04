"""Modules is used to generate DB tables"""

from datetime import datetime
from sqlalchemy import Column, String, Integer
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """User class to generate DB tables"""
    __tablename__ = 'users'
    email = Column(String(120), primary_key=True)
    pwd = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    def __init__(self, email, pwd):
        # constructor
        self.email = email
        self.pwd = pwd

    def __repr__(self):
        return '<User %r>' % (self.email)

class Book(Base):
    __tablename__ = 'books'
    isbn = Column(String(20), primary_key=True)
    name = Column(String(50))
    author = Column(String(50))
    year = Column(Integer)
    def __init__(self, isbn, name, author, year):
        # constructor
        self.isbn = isbn
        self.name = name
        self.author = author
        self.year = year

    def __repr__(self):
        return '<Book %r>' % (self.name)

