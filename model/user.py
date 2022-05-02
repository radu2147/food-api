from typing import Optional

from pydantic.main import BaseModel


class User(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class TokenData(BaseModel):
    username: Optional[str] = None
