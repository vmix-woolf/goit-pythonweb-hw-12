"""
Тести для модуля скидання пароля.
"""
import pytest
from unittest.mock import AsyncMock, patch
from app.services.password_reset import (
    create_reset_token,
    verify_reset_token,
    delete_reset_token,
    send_password_reset_email
)


@pytest.mark.asyncio
async def test_create_reset_token():
    """Тест створення токена скидання пароля."""
    with patch('app.services.password_reset.redis_client') as mock_redis:
        mock_redis.setex = AsyncMock()

        token = await create_reset_token("test@example.com")

        assert isinstance(token, str)
        assert len(token) > 10
        mock_redis.setex.assert_called_once()


@pytest.mark.asyncio
async def test_verify_reset_token_success():
    """Тест успішної перевірки токена."""
    with patch('app.services.password_reset.redis_client') as mock_redis:
        mock_redis.get = AsyncMock(return_value="test@example.com")

        email = await verify_reset_token("valid_token")

        assert email == "test@example.com"
        mock_redis.get.assert_called_once_with("reset:valid_token")


@pytest.mark.asyncio
async def test_verify_reset_token_invalid():
    """Тест перевірки неіснуючого токена."""
    with patch('app.services.password_reset.redis_client') as mock_redis:
        mock_redis.get = AsyncMock(return_value=None)

        email = await verify_reset_token("invalid_token")

        assert email is None


@pytest.mark.asyncio
async def test_delete_reset_token():
    """Тест видалення токена."""
    with patch('app.services.password_reset.redis_client') as mock_redis:
        mock_redis.delete = AsyncMock()

        await delete_reset_token("token_to_delete")

        mock_redis.delete.assert_called_once_with("reset:token_to_delete")


@pytest.mark.asyncio
async def test_send_password_reset_email():
    """Тест надсилання email для скидання пароля."""
    with patch('app.services.password_reset.send_verification_email') as mock_send:
        mock_send.return_value = AsyncMock()

        await send_password_reset_email("test@example.com", "reset_token")

        # Перевіряємо що функція викликалась (хоча б один раз)
        assert mock_send.called