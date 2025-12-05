from unittest.mock import patch, AsyncMock


def test_contacts_endpoint_simple(client):
    """Простий тест endpoints контактів."""

    # Тест без авторизації - має бути 401 (unauthorized)
    response = client.get("/contacts/contacts/")
    assert response.status_code == 401


def test_create_contact_simple(client):
    """Простий тест створення контакту."""

    # Тест без даних - має бути валідаційна помилка
    response = client.post("/contacts/contacts/")
    assert response.status_code in [401, 422]  # unauthorized або validation error