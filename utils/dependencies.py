from tensorflow.python.keras.models import load_model

from repository.repository import Repository
from repository.user_repository import UserRepository

users_db = UserRepository()

model = load_model('weights.h5')
meal_db = Repository()

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


async def get_model():
    try:
        yield model
    finally:
        pass