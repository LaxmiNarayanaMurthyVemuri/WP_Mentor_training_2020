import os
import unittest
from search import *
from application import app
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, or_
from models import Base, User, Book

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

            # Check for environment variable
        if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not set")
        Base.query = db_session.query_property()
        self.app = app.test_client()
    
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass

    
    def test_search_book_by_type_ISBN(self):
        query = "0399"
        books1 = search_book_by_type("ISBN", "0399")
        books2 = db_session.query(Book).filter(or_(Book.isbn.like(f'%{query}'),Book.isbn.like(f'%{query}%'),Book.isbn.like(f'{query}%'), Book.isbn==query))
        self.assertEqual(books1[0], books2[0])

    def test_search_book_by_type_Name(self):
        query = "The"
        books1 = search_book_by_type('Name', "The")
        books2 = db_session.query(Book).filter(or_(Book.name.like(f'%{query}'),Book.name.like(f'%{query}%'),Book.name.like(f'{query}%'), Book.name==query))
        self.assertEqual(books1[0], books2[0])

    def test_search_book_by_type_author(self):
        query = "David"
        books1 = search_book_by_type('author', "David")
        books2 = db_session.query(Book).filter(or_(Book.author.like(f'%{query}'),Book.author.like(f'%{query}%'),Book.author.like(f'{query}%'), Book.author==query))
        self.assertEqual(books1[0], books2[0])

    def test_search_book_by_type_year(self):
        query = "1996"
        books1 = search_book_by_type('year', "1996")
        books2 = db_session.query(Book).filter(Book.year==query)
        self.assertEqual(books1[0], books2[0])
    

if __name__ == "__main__":
    unittest.main()