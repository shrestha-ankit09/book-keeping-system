from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import datetime, timezone


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    isbn = Column(String, unique=True, nullable=False)

    title = Column(String, nullable=False)

    author = Column(String, nullable=False)

    createdAt = Column(DateTime, default=datetime.now(timezone.utc))

    updateAt = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="books")      