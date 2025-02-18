from ariadne import MutationType
from app.model.userModel import User
from app.model.bookModel import Book
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from app.model.schemas import CreateUser, UserBase, CreateBook
from pydantic import ValidationError
from graphql.error import GraphQLError 
from app.utils.util import hash_password, verify_password
from datetime import datetime, timezone

mutation = MutationType()

@mutation.field("registerUser")
async def resolve_create_user(_, info, username: str, email: str, password: str):

    if not username or not email or not password:
        raise GraphQLError(f"Fields should not be empty")

    user_data: dict
    try:
        user_data = CreateUser(
            username=username, 
            email=email, 
            password=password
            )
    except ValidationError as e:
        raise GraphQLError(f"Validation error: {e}")
    

    session: Session = SessionLocal()

    user = session.query(User).filter(User.email == user_data.email).first()

    if user:
        raise GraphQLError("User with this email already exists")


    hashed_password = hash_password(user_data.password)

    new_user = User(
        username=user_data.username, 
        email=user_data.email, 
        password=hashed_password
        )
    
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    session.close()
    return new_user


@mutation.field("loginUser")
def resolve_login_user(_, info, email, password):
    session: Session = SessionLocal()    
    try:
        user_data = UserBase(email=email, password=password)

        user = session.query(User).filter(User.email == user_data.email).first()

        if not user:
            raise GraphQLError("User with that email doesnot exists")
        

        if verify_password(user.password, user_data.password):
            return {**user.__dict__, "token": "Some random token"}
        else:
            raise GraphQLError("Invalid email or password")
    except Exception as e:
        raise GraphQLError(f"Error logging user:: {str(e)}")
    finally:
        session.close()



@mutation.field("createBook")
def resolve_create_book(_, info, input: dict):
    session: Session = SessionLocal()

    try:
        validate_input = CreateBook(**input)
        # Query user by user_id from input
        user = session.query(User).filter(User.id ==  validate_input.user_id).first()

        if not user:
            raise GraphQLError("User with that ID does not exist")

        # Create a new book entry using the input data
        new_book = Book(
            isbn=validate_input.isbn,
            title=validate_input.title,
            author=validate_input.author,
            user_id=validate_input.user_id,
            createdAt=datetime.now(timezone.utc),
            updateAt=datetime.now(timezone.utc)
        )

        # Add the book to the database
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }

        return {**new_book.__dict__, "user": user_data}

    except Exception as e:
        session.rollback()
        raise GraphQLError(f"Error creating book: {str(e)}")

    finally:
        session.close()