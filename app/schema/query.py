from ariadne import QueryType
from app.model.userModel import User
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from graphql.error import GraphQLError 
from app.model.schemas import GetUser
from pydantic import ValidationError

query = QueryType()


@query.field("getUser")
def resolve_get_user(_, info, email: str):
    try:
        user_email = GetUser(email=email)
    except ValidationError as e:
        raise GraphQLError(f"Validation error: {e}")
    
    session: Session = SessionLocal()
    user = session.query(User).filter(User.email == user_email.email).first()

    if not user:
        raise GraphQLError("User with that email doesnot exists")

    return user 



@query.field("getBooks")
def resolve_get_books(_, info):
    pass


@query.field("getBook")
def resolve_get_book(_, info, isbn: str):
    print(isbn)
    pass