import os
import json
import requests
from models import User, Book
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, or_

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))

def get_bookreads_api(isbn):
    if not os.getenv("GOODREADS_KEY"):
        raise RuntimeError("GOODREADS_KEY is not set")
    key = os.getenv("GOODREADS_KEY")
    query = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
    response = query.json()
    response = response['books'][0]
    book_info = db_session.execute("SELECT name, author, year FROM books WHERE isbn = :isbn",{"isbn": isbn}).fetchall()
    response = dict(response)
    response['name'] = book_info[0][0]
    response['author'] = book_info[0][1]
    response['year'] = book_info[0][2]
    response['img'] = "http://covers.openlibrary.org/b/isbn/" + str(isbn) + ".jpg"
    return response

#print(get_bookreads_api("0399153942"))
