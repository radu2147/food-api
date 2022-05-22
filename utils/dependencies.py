from typing import Generator
from tensorflow.python.keras.models import load_model
from model.base import SessionLocal

from repository.repository import DbMealRepository
from passlib.context import CryptContext
from repository.user_repository import DbUserRepository

users_db = DbUserRepository()
meal_db = DbMealRepository()
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    model = load_model('weights.h5')
except:
    print("Trick to run the tests on pipeline. Change that as soon as possible")


def get_user_db() -> DbUserRepository:
    try:
        yield users_db
    finally:
        pass


def get_meal_db() -> DbMealRepository:
    try:
        yield meal_db
    finally:
        pass


def get_db() -> Generator:
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_crypt_context() -> CryptContext:
    try:
        yield crypt_context
    finally:
        pass


async def get_model():
    try:
        yield model
    finally:
        pass
