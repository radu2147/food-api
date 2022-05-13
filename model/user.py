from typing import Optional

from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from model.base import Base


class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class TokenData(BaseModel):
    username: Optional[str] = None

class DbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    meals = relationship("DbMeal", back_populates="owner")
