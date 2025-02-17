from sqlalchemy import Column, Integer, String
from app.database.db import Base
from sqlalchemy.orm import validates, relationship
import re


EMAIL_REGEX = r"(^[\w\.-]+@[\w\.-]+\.\w+$)"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    books = relationship("Book", back_populates="user", cascade="all, delete-orphan")

    @validates("username")
    def validate_username(self, key, username):
        if len(username) < 3 or len(username) > 30:
            raise ValueError("Username must be between 3 and 30 characters.")
        return username

    @validates("email")
    def validate_email(self, key, email):
        if not re.match(EMAIL_REGEX, email):
            raise ValueError("Invalid Email format")
        
        return email
    
