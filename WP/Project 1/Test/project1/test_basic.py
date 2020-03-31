# project1/test_basic.py

import os
import unittest
from application import app, db_session as db

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

    def books(self):
        return self.app.post('/', )
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
    def test_valid_user_login(self):
        response = self.login('admin@msitprogram.net', 'admin')
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_login(self):
        response = self.login('admin@msitprogram.net', 'a1dmin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'wrong password', response.data)

if __name__ == "__main__":
    unittest.main()