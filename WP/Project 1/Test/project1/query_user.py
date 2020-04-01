import os
from models import User
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, or_

engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))

def get_allusers():
    return db_session.query(User)

def get_user_by_email(email):
    return db_session.query(User).filter_by(email=email)

def add_user(new_user):
    db_session.add(new_user)
    db_session.commit()
    db_session.close()
