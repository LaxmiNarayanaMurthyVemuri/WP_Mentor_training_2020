import os
from flask import Flask, session
from flask import render_template
from flask import request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
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

@app.route("/")
def index():
	return "web site under construction"

@app.route("/admin")
def admin():
	users = db_session.query(User)
	return render_template("list.html", value=users)

@app.route("/register",methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template("register.html")
	elif request.method == 'POST':
	    email = request.form['email']
	    pwd = request.form['psw']
	    
	    if(not("@" in email and "." in email)):
	    	return "Please enter valid email"
	    if(db_session.query(User).filter_by(email=email).first() != None):
	    	return "email already registered"

	    new_user = User(email=email, pwd=pwd)
	    db_session.add(new_user)
	    db_session.commit()
	    print(email,pwd)
	    return "Successfully submited your details  " + email