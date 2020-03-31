"""Application page for this flask app"""
import os
from flask import Flask, session
from flask import render_template
from flask import request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import models
from models import Base, User, Book


app = Flask(__name__)

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
        print(qtype,query)
        if qtype == 'ISBN':
            books = db_session.query(Book).filter(or_(Book.isbn.like(f'%{query}'),Book.isbn.like(f'%{query}%'),Book.isbn.like(f'{query}%'), Book.isbn==query))
        elif qtype == 'Name':
            books = db_session.query(Book).filter(or_(Book.name.like(f'%{query}'),Book.name.like(f'%{query}%'),Book.name.like(f'{query}%'), Book.name==query))
        elif qtype == 'author':
            books = db_session.query(Book).filter(or_(Book.author.like(f'%{query}'),Book.author.like(f'%{query}%'),Book.author.like(f'{query}%'), Book.author==query))
        elif qtype == 'year':
            books = db_session.query(Book).filter(Book.year==query)
        if books.first() == None:
            return render_template("home.html", value = None, message = None) 
        else:
            return render_template("home.html", value = books) 

#admin page
@app.route("/admin")
def admin():
    """Return all the users in database"""
    users = db_session.query(User)
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
        if db_session.query(User).filter_by(email=email).first() is not None:
            return render_template("register.html", value="Email already registered please login")

        new_user = User(email=email, pwd=pwd)
        db_session.add(new_user)
        db_session.commit()
        return render_template("register.html", value="Sucessfully registered please login")

#authentication for login
@app.route("/auth", methods=['POST'])
def auth():
    """login authentication for a user"""
    email = request.form['email']
    pwd = request.form['psw']
    if not("@" in email and "." in email):
        return redirect(url_for('register', arg=1))
    if db_session.query(User).filter_by(email=email).first() is None:
        return redirect(url_for('register', arg=2))
    user = db_session.query(User).filter_by(email=email)
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
