from sqlmodel import Session
import strawberry
from graphql_types import AuthorType
from database.models import Author
from database.db import engine

@strawberry.type 
class AuthorMutation:
    
    @strawberry.mutation
    def create_author(self, name: str, age: int, nationality: str) -> AuthorType:
        with Session(engine) as session:
            new_author = Author(name=name, age=age, nationality=nationality)
            
            session.add(new_author)
            session.commit()
            session.refresh(new_author)

            return AuthorType(
                id=new_author.id, 
                name=new_author.name, 
                age=new_author.age,
                nationality=new_author.nationality,
                books=[]
            )
    
    @strawberry.mutation
    def delete_author(self, author_id: int) -> str:
        with Session(engine) as session:
            author = session.get(Author, author_id)
            
            if not author:
                raise ValueError(f"Author with ID {author_id} not found.")
            
            for book in author.books:
                session.delete(book)
            
            session.delete(author)
            session.commit()
            
            return f"{author.name} and all their books have been successfully deleted!"
