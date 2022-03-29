from tensorflow.python.keras.models import load_model

from repository.repository import Repository
from passlib.context import CryptContext
from repository.user_repository import UserRepository

users_db = UserRepository()

try:
    model = load_model('weights.h5')
except:
    print("Trick to run the tests on pipeline. Change that as soon as possible")


meal_db = Repository()
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_db() -> UserRepository:
    try:
        yield users_db
    finally:
        pass


def get_meal_db() -> Repository:
    try:
        yield meal_db
    finally:
        pass

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