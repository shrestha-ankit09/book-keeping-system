from ariadne import QueryType
from app.model.userModel import User
from app.database.db import SessionLocal
from sqlalchemy.orm import Session

query = QueryType()


@query.field("getUser")
def resolve_get_user(_, info, email: str):
    session: Session = SessionLocal()
    user = session.query(User).filter(User.email == email).first()
    return user 



@query.field("getBooks")
def resolve_get_books(_, info):
    pass


@query.field("getBook")
def resolve_get_book(_, info, isbn: str):
    print(isbn)
    pass