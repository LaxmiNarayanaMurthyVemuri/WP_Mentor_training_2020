"""Application page for this flask app"""
import os
from flask import Flask, session, jsonify, render_template, request, redirect, url_for, request
from flask_session import Session
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import models
from models import Base, User, Book
from search import *
from book_details import *
from query_user import *


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)
init_db()



#Home page
@app.route("/", methods=['GET', 'POST'])
def index():
    """Return to home if already logged in else to registration"""
    if request.method == 'GET':
        if session.get("email") is None:
            return redirect(url_for('register', arg=4))
        return render_template("home.html", value = None)
    elif request.method == 'POST':
        qtype = request.form['type']
        query = request.form['query']
        books = search_book_by_type(qtype, query)
        if books.first() == None:
            return render_template("home.html", value = None, message = None) 
        else:
            return render_template("home.html", value = books) 



#admin page
@app.route("/admin")
def admin():
    """Return all the users in database"""
    users = get_allusers()
    return render_template("list.html", value=users)

#registration page
@app.route("/register", methods=['GET', 'POST'])
@app.route("/register/<int:arg>", methods=['GET', 'POST'])
def register(arg=None):
    """register a user in to database"""
    if request.method == 'GET':
        if arg == 1:
            arg = 'Please enter valid email'
        elif arg == 2:
            arg = 'Email is not register. Please register'
        elif arg == 3:
            arg = 'wrong password'
        elif arg == 4:
            arg = 'please login'
        return render_template("register.html", value=arg)
    elif request.method == 'POST':
        email = request.form['email']
        pwd = request.form['psw']
        if not("@" in email and "." in email):
            return render_template("register.html", value="Please enter valid email")
        if get_user_by_email(email) is not None:
            return render_template("register.html", value="Email already registered please login")

        
        new_user = User(email=email, pwd=pwd)
        add_user(new_user)
        return render_template("register.html", value="Sucessfully registered please login")

#authentication for login
@app.route("/auth", methods=['POST'])
def auth():
    """login authentication for a user"""
    email = request.form['email']
    pwd = request.form['psw']
    if not("@" in email and "." in email):
        return redirect(url_for('register', arg=1))
    user = get_user_by_email(email)
    if user is None:
        return redirect(url_for('register', arg=2))
    if user[0].email == email and user[0].pwd == pwd:
        session["email"] = user[0].email
        session["pwd"] = user[0].pwd
        return redirect(url_for('index'))
    return redirect(url_for('register', arg=3))

# Logout
@app.route("/logout")
def logout():
    """Logout a user"""
    session.clear()
    return redirect(url_for("register"))

# To show a book details
@app.route("/books", methods=["GET"])
def book_details():
    isbn = request.args.get('isbn')
    book = get_book_by_isbn(isbn)
    # book.isbn, book.name, book.author, book.year = db_session.execute("SELECT isbn, name, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if request.method == "GET":
        return render_template("book_detail.html", book=book[0])

#sending as parameters as string, so we have used GET request
@app.route("/api/book/", methods=["GET"])
def api_get_book():
    isbn = request.args.get('isbn') 
    book = get_book_by_isbn(isbn)
    if request.method == "GET":
        if book.count() != 1:
            return (jsonify({"Error": "Invalid book ISBN"}), 422)
        else:
            book = book[0]
            return jsonify(title=book.name, author=book.author, year=book.year, isbn=book.isbn)

# sending data as JSON, so we have used POST request
@app.route("/api/search/", methods=["POST"])
@cross_origin()
def api_search_isbn():
    if request.is_json:
        content = request.get_json()
        if 'type' in content and 'query' in content:
            # type can be ISBN, Name, author, year
            qtype = content['type'].strip()
            if qtype in ["ISBN", "Name", "author","year"]:
                query = content['query'].strip()
                books = search_book_by_type(qtype, query)
                if books is not None:
                    l = []
                    books_json = {}
                    for book in books:
                        d = {}
                        d["isbn"] = book.isbn
                        l.append(d)
                    books_json['books'] = l
                    return jsonify(books_json)
            else:
                return (jsonify({"Error": "Invalid key value"}), 400)
        else:
            return (jsonify({"Error": "Invalid JSON data"}), 400)
    else:
        return (jsonify({"Error": "Invalid JSON type"}), 422)