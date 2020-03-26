from application import Base
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.types import TIMESTAMP
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    email = Column(String(120), primary_key=True)
    pwd = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    def __init__(self, email, pwd):
        self.email = email
        self.pwd = pwd

    def __repr__(self):
        return '<User %r>' % (self.email)