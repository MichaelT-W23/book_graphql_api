from fastapi import HTTPException
from sqlmodel import Session, select
import strawberry
from graphql_types import AuthorType, BookType
from database.models import Book
from database.db import engine

@strawberry.type
class BookQuery:

    @strawberry.field
    def get_all_books(self) -> list[BookType]:
        with Session(engine) as session:
            statement = select(Book)
            results = session.exec(statement).all()

            return [
                BookType(
                    id=book.id,
                    title=book.title,
                    publicationYear=book.publicationYear,
                    genre=book.genre,
                    author=AuthorType(
                        id=book.author.id,
                        name=book.author.name,
                        age=book.author.age,
                        nationality=book.author.nationality
                    )
                )
                for book in results
            ]
    
    @strawberry.field
    def get_book(self, id: int) -> BookType:
        with Session(engine) as session:
            statement = select(Book).where(Book.id == id)
            book = session.exec(statement).first()

            if not book:
                raise HTTPException(status_code=404, detail="Book not found")

            return BookType(
                id=book.id,
                title=book.title,
                publicationYear=book.publicationYear,
                genre=book.genre,
                author=AuthorType(
                    id=book.author.id,
                    name=book.author.name,
                    age=book.author.age,
                    nationality=book.author.nationality
                )
            )

    
    @strawberry.field
    def get_all_genres(self) -> list[str]:
        with Session(engine) as session:
            statement = select(Book.genre).distinct()
            all_genres = session.exec(statement).all()
            
            return all_genres
        
    @strawberry.field
    def get_books_by_genre(self, genre: str) -> list[BookType]:
        with Session(engine) as session:
            statement = select(Book).where(Book.genre == genre)
            results = session.exec(statement).all()

            if not results:
                raise HTTPException(status_code=404, detail="No books found for the specified genre")
            
            return [
                BookType(
                    id=book.id,
                    title=book.title,
                    publicationYear=book.publicationYear,
                    genre=book.genre,
                    author=AuthorType(
                        id=book.author.id,
                        name=book.author.name,
                        age=book.author.age,
                        nationality=book.author.nationality
                    )
                )
                for book in results
            ]