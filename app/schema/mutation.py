from ariadne import MutationType
from app.model.userModel import User
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from app.model.schemas import CreateUser, UserBase
from pydantic import ValidationError
from graphql.error import GraphQLError 
from app.utils.util import hash_password, verify_password

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
    user_data: dict
    if not email or not password:
        raise GraphQLError("Fields should be empty")
    
    try:
        user_data = UserBase(email=email, password=password)
    except ValidationError as e:
        raise GraphQLError(f"Validation error: {e}") 


    session: Session = SessionLocal()
    user = session.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise GraphQLError("User with that email doesnot exists")
    

    if verify_password(user.password, user_data.password):
        return {**user.__dict__, "token": "Some random token"}
    else:
        raise GraphQLError("Invalid email or password")

    

    