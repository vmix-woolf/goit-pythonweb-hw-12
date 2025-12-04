import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from app.main import app


# ---------------------------
# Настройка event loop
# ---------------------------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ---------------------------
# MOCK FIXTURES (UNIT TESTS)
# ---------------------------
@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.delete = AsyncMock()
    session.add = AsyncMock()
    return session


@pytest.fixture
def mock_cloudinary_upload():
    with patch("cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {"secure_url": "https://example.com/avatar.png"}
        yield mock_upload


@pytest.fixture
def mock_user():
    from app.models.user import User
    return User(
        id=1,
        email="test@example.com",
        username="tester",
        password="hashed_password",
        is_verified=True,
    )


# ---------------------------
# ASYNC CLIENT (INTEGRATION)
# ---------------------------
@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
