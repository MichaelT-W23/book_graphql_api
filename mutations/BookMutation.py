from pydantic import ValidationError
from sqlmodel import Session
import strawberry
from graphql_types import AuthorType, BookType
from database.models import Book
from database.db import engine

@strawberry.type 
class BookMutation:

    @strawberry.mutation
    def create_book(self, title: str, publicationYear: int, genre: str, author_id: int) -> BookType:
        try:
            validated_book = Book.model_validate({
                "title": title,
                "publicationYear": publicationYear,
                "genre": genre,
                "author_id": author_id
            })
            
            with Session(engine) as session:
                session.add(validated_book)
                session.commit()
                session.refresh(validated_book)

                author = validated_book.author

                return BookType(
                    id=validated_book.id,
                    title=validated_book.title,
                    publicationYear=validated_book.publicationYear,
                    genre=validated_book.genre,
                    author=AuthorType(
                        id=author.id,
                        name=author.name,
                        age=author.age,
                        nationality=author.nationality
                    )
                )
            
        except ValidationError as e:
            raise ValueError(f"Validation Error: {e}")


    @strawberry.mutation
    def delete_book(self, book_id: int) -> str:
        with Session(engine) as session:
            book_to_delete = session.get(Book, book_id)

            if not book_to_delete:
                return f"Book with ID {book_id} does not exist."
            
            session.delete(book_to_delete)
            session.commit()
            
            return f"Book with ID {book_id} has been successfully deleted!"
