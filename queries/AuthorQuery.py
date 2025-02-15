from fastapi import HTTPException
from sqlmodel import Session, select
import strawberry
from graphql_types import AuthorType, BookType
from database.models import Author
from database.db import engine


@strawberry.type
class AuthorQuery:

    @strawberry.field
    def get_all_authors(self) -> list[AuthorType]:
        with Session(engine) as session:
            statement = select(Author)
            results = session.exec(statement).all()

            return [
                AuthorType(
                    id=author.id,
                    name=author.name,
                    age=author.age,
                    nationality=author.nationality,
                    books=[
                        BookType(
                            id=book.id,
                            title=book.title,
                            publicationYear=book.publicationYear,
                            genre=book.genre,
                            author=None  # Set author to None to prevent infinite recursion
                        )
                        for book in author.books
                    ] if author.books else None
                )
                for author in results
            ]

    @strawberry.field
    def get_author(self, id: int) -> AuthorType:
        with Session(engine) as session:
            author = session.get(Author, id)

            if not author:
                raise HTTPException(status_code=404, detail="Author not found")
            
            return AuthorType(
                id=author.id,
                name=author.name,
                age=author.age,
                nationality=author.nationality,
                books=[
                    BookType(
                        id=book.id,
                        title=book.title,
                        publicationYear=book.publicationYear,
                        genre=book.genre,
                        author=None  # Prevent recursion issues
                    )
                    for book in author.books
                ] if author.books else None
            )
