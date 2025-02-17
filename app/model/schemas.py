from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str

    class Config: 
        orm_mode = True



class BookBase(BaseModel):
    id: int
    isbn: str
    title: str
    author:str

    class config:
        orm_mode = True