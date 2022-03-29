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

def test_register_already_existing_user():
    response = client.post('/register', json={"username": "radu", "password": "baston"})
    assert response.status_code == 401

def test_login_existing_user():
    response = client.post('/login', json={"username": "radu", "password": "baston"})
    assert response.status_code == 200

def test_login_unexisting_user():
    response = client.post('/login', json={"username": "no_user", "password": "baston"})
    assert response.status_code == 401

def test_login_insufficient_fields():
    response = client.post('/login', json={"password": "baston"})
    assert response.status_code == 422

def test_add_meal():
    response = client.post('/login', json={"username": "radu", "password": "baston"})
    
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
            "user": {
                "username": "",
                "password": ""
            }
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
	        "nutritional_values":{
		        "kcal": 576,
		        "protein": 12.3,
		        "carbs": 12,
		        "fats": 14.2
	        },
            "user": {
                "username": "",
                "password": ""
            }
        },
    )
    assert response.status_code == 401

def test_add_meal_wrong_fields():
    response = client.post('/login', json={"username": "radu", "password": "baston"})
    
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
    response = client.post('/login', json={"username": "radu", "password": "baston"})
    
    token = response.json()['access_token']
    response = client.get('/meal?datetime=2022-03-26T00:00:00', 
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_meal_date_no_answer():
    response = client.post('/login', json={"username": "radu", "password": "baston"})
    
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