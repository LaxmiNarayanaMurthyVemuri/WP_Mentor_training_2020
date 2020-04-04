import os
import unittest
from book_details import *
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

    def test_get_book_by_isbn(self):
        book1 = get_book_by_isbn("0399153942")
        book2 = db_session.query(Book).filter_by(isbn="0399153942")
        self.assertEqual(book1[0], book2[0])
    

if __name__ == "__main__":
    unittest.main()