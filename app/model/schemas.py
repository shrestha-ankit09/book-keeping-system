from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel): 
    email: EmailStr
    password: str

    class Config: 
        orm_mode = True


class CreateUser(UserBase):
    username: str = Field(..., min_length=3, max_length=30)

    class Config:
        orm_mode = True


class GetUser(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    isbn: str
    title: str
    author:str




class CreateBook(BookBase):
    user_id: int
    class Config:
        orm_mode = True