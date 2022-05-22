from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from model.base import SessionLocal

from model.user import User, TokenData
from repository.user_repository import DbUserRepository
from utils.constants import SECRET_KEY, ALGORITHM
from utils.dependencies import get_crypt_context, get_user_db, get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str, pwd_context: CryptContext):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(pwd_context: CryptContext, password: str):
    return pwd_context.hash(password)


def get_user(db: Session, repo: DbUserRepository, username: str) -> Optional[User]:
    return repo.get(db, username)


def authenticate_user(db: Session, user_repo: DbUserRepository, username: str, password: str, crypt_context: CryptContext) -> Optional[User]:
    user = get_user(db, user_repo, username)
    if not user:
        return None
    if not verify_password(password, user.password, crypt_context):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), user_repo: DbUserRepository = Depends(get_user_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, user_repo, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user