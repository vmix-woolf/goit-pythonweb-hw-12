import pytest
from unittest.mock import AsyncMock, patch
from datetime import timedelta

from app.services.auth import (
    create_access_token,
    verify_token,
    get_current_user,
)
from app.schemas.user import TokenData
from app.models.user import User


def test_create_access_token_returns_string():
    """Перевіряємо, що create_access_token повертає токен."""
    token = create_access_token({"sub": "test@example.com"})
    assert isinstance(token, str)
    assert len(token) > 10


def test_create_access_token_expiration_custom():
    """Перевіряємо, що токен створюється з кастомним часом життя."""
    token = create_access_token(
        {"sub": "test@example.com"},
        expires_delta=timedelta(minutes=1),
    )
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_verify_token_valid():
    """Перевіряємо валідний токен."""
    token = create_access_token({"sub": "test@example.com"})
    data = await verify_token(token)

    assert isinstance(data, TokenData)
    assert data.email == "test@example.com"


@pytest.mark.asyncio
async def test_verify_token_invalid():
    """Невалідний токен → HTTPException."""
    with pytest.raises(Exception):
        await verify_token("invalid.token.value")


@pytest.mark.asyncio
async def test_get_current_user_success():
    """Перевіряємо, що get_current_user повертає користувача."""

    fake_user = User(
        id=1,
        email="user@example.com",
        username="test",
        password="hashed",
        is_verified=True,
    )

    # 1. verify_token повертає TokenData
    with patch("app.services.auth.verify_token", return_value=TokenData(email="user@example.com")):
        # 2. get_user_by_email повертає користувача
        with patch("app.services.auth.get_user_by_email", AsyncMock(return_value=fake_user)):
            user = await get_current_user("fake.jwt.token")

    assert isinstance(user, User)
    assert user.email == "user@example.com"


@pytest.mark.asyncio
async def test_get_current_user_not_found():
    """Користувач не знайдений → HTTPException 404."""
    with patch("app.services.auth.verify_token", return_value=TokenData(email="ghost@example.com")):
        with patch("app.services.auth.get_user_by_email", AsyncMock(return_value=None)):
            with pytest.raises(Exception):
                await get_current_user("fake.jwt.token")
