from fastapi.testclient import TestClient


def test_signup(client: TestClient):
    """Тест реєстрації користувача."""
    data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123"
    }

    response = client.post("/auth/signup", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == data["email"]
    assert response.json()["username"] == data["username"]


def test_login(client: TestClient):
    """Тест логіну користувача."""
    # Спочатку реєструємо користувача
    signup_data = {
        "email": "loginuser@example.com",
        "username": "loginuser",
        "password": "mypassword"
    }
    signup_response = client.post("/auth/signup", json=signup_data)
    assert signup_response.status_code == 201

    # Потім логінимося
    login_data = {
        "username": signup_data["email"],  # FastAPI OAuth2PasswordRequestForm використовує username field
        "password": signup_data["password"]
    }

    response = client.post("/auth/login", data=login_data)  # form data, не json

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    """Тест логіну з неправильним паролем."""
    # Спочатку реєструємо користувача
    signup_data = {
        "email": "wrongpass@example.com",
        "username": "wrongpass",
        "password": "correctpass"
    }
    signup_response = client.post("/auth/signup", json=signup_data)
    assert signup_response.status_code == 201

    # Потім пробуємо увійти з неправильним паролем
    login_data = {
        "username": "wrongpass@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient):
    """Тест логіну неіснуючого користувача."""
    login_data = {
        "username": "ghost@example.com",
        "password": "anypassword"
    }

    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401