import pytest
import os
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.database import get_session

# Устанавливаем флаг для тестов
os.environ["TESTING"] = "true"


# ----------------------------------------------------
# Event loop - session scope для стабільності
# ----------------------------------------------------
@pytest.fixture(scope="session")
def event_loop():
    """Фіксований event loop для всієї сесії тестів."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# ----------------------------------------------------
# Ініціалізація тестової БД - session scope
# ----------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    """Ініціалізація тестової БД."""
    from tests.db import init_test_db, override_get_session

    await init_test_db()

    # Override dependency глобально для всіх інтеграційних тестів
    app.dependency_overrides[get_session] = override_get_session

    yield

    # Cleanup
    app.dependency_overrides.clear()


# ----------------------------------------------------
# TestClient - стандартний підхід FastAPI
# ----------------------------------------------------
@pytest.fixture(scope="session")
def client():
    """Синхронний TestClient для інтеграційних тестів."""
    with TestClient(app) as test_client:
        yield test_client


# ----------------------------------------------------
# Helper функція для авторизації - спрощена версія
# ----------------------------------------------------
def register_and_login(client: TestClient, email: str = "test@example.com", password: str = "secret"):
    """Допоміжна функція для реєстрації та отримання токена."""
    signup_data = {
        "email": email,
        "username": email.split("@")[0],
        "password": password
    }

    signup_response = client.post("/auth/signup", json=signup_data)

    if signup_response.status_code != 201:
        print(f"Signup failed: {signup_response.status_code} - {signup_response.text}")
        return None

    login_data = {
        "username": email,
        "password": password
    }
    login_response = client.post("/auth/login", data=login_data)

    if login_response.status_code != 200:
        print(f"Login failed: {login_response.status_code} - {login_response.text}")
        return None

    return login_response.json()["access_token"]


# ----------------------------------------------------
# Юніт-тестові моки
# ----------------------------------------------------
@pytest.fixture
def mock_session():
    """Мок session для юніт-тестів."""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.delete = AsyncMock()
    session.add = AsyncMock()
    return session


@pytest.fixture
def mock_cloudinary_upload():
    """Мок Cloudinary."""
    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {"secure_url": "https://example.com/avatar.png"}
        yield mock_upload


@pytest.fixture
def mock_user():
    """Мок користувача."""
    from app.models.user import User
    return User(
        id=1,
        email="test@example.com",
        username="tester",
        password="hashed_password",
        is_verified=True,
    )