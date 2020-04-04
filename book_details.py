import os
from models import Book
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, or_

engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))

def get_book_by_isbn(isbn):
    return db_session.query(Book).filter_by(isbn=isbn)