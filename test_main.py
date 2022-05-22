import random
import string
from typing import Generator
import app
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.base import Base

from utils.dependencies import get_db

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/test_food'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

username = random_lower_string()

def override_get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.app.dependency_overrides[get_db] = override_get_db

client = TestClient(app.app)

def test_register_user():
    response = client.post('/register', json={"username": username, "password": "baston"})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_register_user_not_enough_fields():
    response = client.post('/register', json={"password": "baston"})
    assert response.status_code == 422

def test_predict_food():
    filename = "example_food.jpg"
    response = client.post(
    "/uploadfile/", files={"file": ("filename", open(filename, "rb"), "image/jpeg")})

    resp = response.json()
    assert response.status_code == 200
    assert resp["foodClass"] == 'Apple Pie'

def test_predict_non_food():
    filename = "example_non_food.jpg"
    response = client.post(
    "/uploadfile/", files={"file": ("filename", open(filename, "rb"), "image/jpeg")})

    assert response.status_code == 400


def test_register_already_existing_user():
    response = client.post('/register', json={"username": username, "password": "baston"})
    assert response.status_code == 401

def test_login_existing_user():
    response = client.post('/login', json={"username": username, "password": "baston"})
    assert response.status_code == 200

def test_login_existing_user_wrong_password():
    response = client.post('/login', json={"username": username, "password": "error"})
    assert response.status_code == 401

def test_login_unexisting_user():
    response = client.post('/login', json={"username": "no_user", "password": "baston"})
    assert response.status_code == 401

def test_login_insufficient_fields():
    response = client.post('/login', json={"password": "baston"})
    assert response.status_code == 422

def test_add_meal():
    response = client.post('/login', json={"username": username, "password": "baston"})
    
    token = response.json()['access_token']
    response = client.post('/meal', 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "id": -1,
	        "date": "2022-03-26T00:00:00",
	        "meal_type": "Breakfast",
	        "name": "Test food",
            "kcal": 576,
            "protein": 12.3,
            "carbs": 12,
            "fat": 14.2,
            "user": {
                "username": "",
                "password": ""
            },
            "quantity": 1
        },
    )
    assert response.status_code == 200

def test_add_meal_wrong_token():

    response = client.post('/meal', 
        headers={"Authorization": f"Bearer "},
        json={
            "id": -1,
	        "date": "2022-03-26T00:00:00",
	        "meal_type": "Breakfast",
	        "name": "Test food",
            "kcal": 576,
            "protein": 12.3,
            "carbs": 12,
            "fat": 14.2,
            "user": {
                "username": "",
                "password": ""
            }
        },
    )
    assert response.status_code == 401

def test_add_meal_wrong_fields():
    response = client.post('/login', json={"username": username, "password": "baston"})
    
    token = response.json()['access_token']
    response = client.post('/meal', 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "id": -1,
	        "date": "2022-03-26T00:00:00",
	        "meal_type": "Breakfast",
	        "name": "Test food",
	        "nutritional_values":{
		        "kcal": 576,
		        "protein": 12.3,
		        "carbs": 12,
		        "fats": 14.2
	        },
        },
    )
    assert response.status_code == 422

def test_get_meal_date():
    response = client.post('/login', json={"username": username, "password": "baston"})
    
    token = response.json()['access_token']
    response = client.get('/meal?datetime=2022-03-26T00:00:00', 
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_meal_date_no_answer():
    response = client.post('/login', json={"username": username, "password": "baston"})
    
    token = response.json()['access_token']
    response = client.get('/meal?datetime=2021-03-26T00:00:00', 
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_get_meal_date_no_token():
    response = client.get('/meal?datetime=2021-03-26T00:00:00',
    )
    assert response.status_code == 401