from typing import List, Optional
import strawberry

@strawberry.type
class AuthorType:
    id: int
    name: str
    age: int
    nationality: str
    books: Optional[List["BookType"]] = None # Quotes because its a forward reference

@strawberry.type
class BookType:
    id: int
    title: str
    publicationYear: int
    genre: str
    author: AuthorType