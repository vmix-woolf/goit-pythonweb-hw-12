import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient

from app.main import app
from app.models.user import User


# подменяем event loop для pytest-asyncio
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# мок-сесія SQLAlchemy
@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.delete = AsyncMock()
    session.add = AsyncMock()
    return session


# мок користувача для unit-тестів
@pytest.fixture
def mock_user():
    return User(
        id=1,
        email="test@example.com",
        username="tester",
        password="hashed_password",
        is_verified=True,
    )


# мок Cloudinary uploader
@pytest.fixture
def mock_cloudinary_upload():
    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {"secure_url": "https://example.com/avatar.png"}
        yield mock_upload


# async-клієнт для інтеграційних тестів
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
