from typing import List, Optional
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    publicationYear: int
    genre: str

    author_id: int = Field(foreign_key="author.id")

    author: "Author" = Relationship(back_populates="books")

    # this will let us use the "model_validate" function
    @field_validator("genre", mode="before")
    def capitalize_genre(cls, value: str) -> str:
        if value:
            return value.capitalize()
        return value

class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    nationality: str

    books: List[Book] = Relationship(back_populates="author")
