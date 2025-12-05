from fastapi.testclient import TestClient
from tests.conftest import register_and_login


def test_create_contact(client: TestClient):
    """Тест створення контакту."""
    # Отримуємо токен авторизації
    token = register_and_login(client, "u1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Дані для створення контакту
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@ex.com",
        "phone": "111"
    }

    response = client.post("/contacts/", json=contact_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["email"] == "john@ex.com"


def test_get_contacts(client: TestClient):
    """Тест отримання списку контактів."""
    # Отримуємо токен авторизації
    token = register_and_login(client, "u2@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/contacts/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_contact(client: TestClient):
    """Тест оновлення контакту."""
    # Отримуємо токен авторизації
    token = register_and_login(client, "u3@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Створюємо контакт
    create_response = client.post("/contacts/", json={
        "first_name": "A",
        "last_name": "B",
        "email": "a@b.com",
        "phone": "1"
    }, headers=headers)

    contact_id = create_response.json()["id"]

    # Оновлюємо контакт
    update_response = client.put(f"/contacts/{contact_id}", json={
        "first_name": "X"
    }, headers=headers)

    assert update_response.status_code == 200
    assert update_response.json()["first_name"] == "X"


def test_delete_contact(client: TestClient):
    """Тест видалення контакту."""
    # Отримуємо токен авторизації
    token = register_and_login(client, "u4@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Створюємо контакт
    create_response = client.post("/contacts/", json={
        "first_name": "Z",
        "last_name": "Q",
        "email": "z@q.com",
        "phone": "333"
    }, headers=headers)

    contact_id = create_response.json()["id"]

    # Видаляємо контакт
    delete_response = client.delete(f"/contacts/{contact_id}", headers=headers)
    assert delete_response.status_code == 204