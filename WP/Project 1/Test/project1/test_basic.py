# project1/test_basic.py

import os
import unittest
from application import *
from models import Base, User, Book

class BasicTests(unittest.TestCase):
 
############################
#### setup and teardown ####
############################
 
    # executed prior to each test
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
 
########################
#### helper methods ####
########################
     
    def register(self, email, password):
        return self.app.post('/register',data=dict(email=email, psw=password),follow_redirects=True)
     
    def login(self, email, password):
        return self.app.post('/auth',data=dict(email=email, psw=password),follow_redirects=True)
     
    def logout(self):
        return self.app.get('/logout',follow_redirects=True)

    def books(self, type1, year):
        return self.app.post('/', data=dict(type=type1, query=year),follow_redirects=True)

    def books_detail(self, type1):
        return self.app.get('/books', data=dict(isbn=type1),follow_redirects=True)
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)

    def test_admin(self):
        response = self.app.get("/admin")
        self.assertEqual(response.status_code, 200)

    def test_login_invalid(self):
        response = self.login('adminmsitprogram.net', 'a1dmin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter valid email', response.data)

    def test_login(self):
        response = self.login('murthy@msitprogram.net', 'a1dmin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email is not register. Please register', response.data)

    def test_register(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_register(self):
        response = self.register('admin@msitprogram.net', 'a1dmin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email already registered please login', response.data)

    def test_invalid_user_registeremail(self):
        response = self.register('adminmsitprogram.net', 'a1dmin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter valid email', response.data)

    def test_invalid_user_registeremail_fun(self):
        response = self.register('adminmsitprogramnet', 'a1dmin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter valid email', response.data)

    def test_valid_user_login(self):
        response = self.login('admin@msitprogram.net', 'admin')
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_login(self):
        response = self.login('admin@msitprogram.net', 'a1dmin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'wrong password', response.data)

    def test_valid_search(self):
        response = self.books('year', 1994)
        books = db_session.query(Book).filter(Book.year==1994)
        self.assertEqual(response.status_code, 200)

    def test_invalid_search_year(self):
        response = self.books('year', 2020)
        books = db_session.query(Book).filter(Book.year==2020)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No results found for your search', response.data)

    def test_invalid_search_isbn(self):
        response = self.books('ISBN', "2058X")
        books = db_session.query(Book).filter(Book.isbn=="2058X")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No results found for your search', response.data)

    def test_invalid_search_author(self):
        response = self.books('author', "Murthy")
        books = db_session.query(Book).filter(Book.author=="Murthy")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No results found for your search', response.data)

    def test_invalid_search_name(self):
        response = self.books('Name', "Vemuri")
        books = db_session.query(Book).filter(Book.name=="Vemuri")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No results found for your search', response.data)

    def test_bookdetails(self):
        response = self.app.get('/books', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_bookdetails(self):
        response = self.books_detail('0743484363')
        book = db_session.query(Book).filter_by(isbn="0743484363").first()
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()