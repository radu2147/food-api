from typing import Optional

from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from model.base import Base

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class TokenData(BaseModel):
    username: Optional[str] = None

class DbUser(Base):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, primary_key=True)
    hashed_password = Column(String, nullable = False)

    meals = relationship("DbMeal", back_populates="user")

class User(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

    @staticmethod
    def fromDb(user: DbUser) -> "User":
        return User(
            username=user.username,
            password=user.hashed_password
        )