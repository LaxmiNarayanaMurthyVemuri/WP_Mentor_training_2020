import os
from models import Book
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, or_

engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))

def search_book_by_type(qtype, query):
    if qtype == 'ISBN':
        books = db_session.query(Book).filter(or_(Book.isbn.like(f'%{query}'),Book.isbn.like(f'%{query}%'),Book.isbn.like(f'{query}%'), Book.isbn==query))
    elif qtype == 'Name':
        books = db_session.query(Book).filter(or_(Book.name.like(f'%{query}'),Book.name.like(f'%{query}%'),Book.name.like(f'{query}%'), Book.name==query))
    elif qtype == 'author':
        books = db_session.query(Book).filter(or_(Book.author.like(f'%{query}'),Book.author.like(f'%{query}%'),Book.author.like(f'{query}%'), Book.author==query))
    elif qtype == 'year':
        books = db_session.query(Book).filter(Book.year==query)
    return books

def get_book_by_isbn(isbn):
    return db_session.query(Book).filter_by(isbn=isbn).first()