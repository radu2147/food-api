import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_register_user():
    response = client.post('/register', json={"username": "radu", "password": "baston"})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_register_user_not_enough_fields():
    response = client.post('/register', json={"password": "baston"})
    assert response.status_code == 422
