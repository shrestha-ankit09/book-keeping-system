from ariadne import QueryType
from app.model.userModel import User
from app.model.bookModel import Book
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
    session: Session = SessionLocal()

    try:
        books = session.query(Book).all()

        if not books:
            return []
        
        books_data = [
            {key:value for key, value in book.__dict__.items() if not key.startswith('_')} 
            for book in books
        ]

        return books_data
    except Exception as e:
        raise GraphQLError(f"Error fetching book data: {str(e)}")
    finally:
        session.close()


@query.field("getBook")
def resolve_get_book(_, info, isbn: str):
    session: Session = SessionLocal()

    try:
        book = session.query(Book).filter(Book.isbn == isbn).first()

        if not book:
            return {"message": "Book not found with that isbn number"}
        
        book_data = {key:value for key, value in book.__dict__.items() if not key.startswith('_')}

        return book_data

    except Exception as e:
        raise GraphQLError(f"Error Fetching data of isbn number {isbn}, error: {str(e)}")
    finally:
        session.close()
