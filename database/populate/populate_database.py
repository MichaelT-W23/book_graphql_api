import json
from sqlmodel import Session
from ..models import Author, Book
from ..db import engine
from termcolor import colored as c

def add_authors_and_books(authors, books_dict):

    with Session(engine) as session:

        for author_data in authors:
            author = Author(**author_data)
            session.add(author)

        session.commit()

        for book_data in books_dict:
            book = Book(**Book.model_validate(book_data).model_dump())
            session.add(book)

        session.commit()

        print(c("Data inserted successfully from JSON and dictionary!", 'green'))


with open('database/populate/data.json', 'r') as file:
    content = json.load(file)

authors = content['authors']
books = content['books']

add_authors_and_books(authors, books)
