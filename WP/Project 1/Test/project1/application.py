import os

from flask import Flask, session
from flask import render_template
from flask import request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



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


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
init_db()

@app.route("/")
def index():
	return "web site under construction"



@app.route("/register",methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template("register.html")
	elif request.method == 'POST':
	    email = request.form['email']
	    psw = request.form['psw']
	    print(email,psw)
	    return "Successfully submited your details  " + email