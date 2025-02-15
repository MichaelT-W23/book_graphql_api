import strawberry

from queries.AuthorQuery import AuthorQuery
from queries.BookQuery import BookQuery

from mutations.AuthorMutation import AuthorMutation
from mutations.BookMutation import BookMutation

@strawberry.type
class Query(AuthorQuery, BookQuery):
    pass

@strawberry.type
class Mutation(AuthorMutation, BookMutation):
    pass

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)