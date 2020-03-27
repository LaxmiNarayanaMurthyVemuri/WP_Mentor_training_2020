"""Application page for this flask app"""
import os
from flask import Flask, session
from flask import render_template
from flask import request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import User


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)

#Home page
@app.route("/")
def index():
    """Return to home if already logged in else to registration"""
    if session.get("email") is None:
        return redirect(url_for('register', arg=4))
    return render_template("home.html")

#admin page
@app.route("/admin")
def admin():
    """Return all the users in database"""
    users = db_session.query(User)
    return render_template("list.html", value=users)

#registration page
@app.route("/register", methods=['GET', 'POST'])
@app.route("/register/<int:a>", methods=['GET', 'POST'])
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
        if db_session.query(User).filter_by(email=email) != None:
            return render_template("register.html", value="Email already registered please login")

        new_user = User(email=email, pwd=pwd)
        db_session.add(new_user)
        return render_template("register.html", value="Sucessfully registered please login")

#authentication for login
@app.route("/auth", methods=['POST'])
def auth():
    """login authentication for a user"""
    email = request.form['email']
    pwd = request.form['psw']
    if not("@" in email and "." in email):
        return redirect(url_for('register', arg=1))
    if db_session.query(User).filter_by(email=email) is None:
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
