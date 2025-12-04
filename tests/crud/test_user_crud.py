import pytest
from unittest.mock import MagicMock, AsyncMock

from app.crud.user import (
    hash_password,
    verify_password,
    get_user_by_email,
    create_user,
    authenticate_user,
)
from app.models.user import User
from app.schemas.user import UserCreate


# ------------------ hash_password ------------------ #

def test_hash_password_creates_different_hashes():
    """
    Перевіряємо, що bcrypt генерує різний хеш для однакових паролів.
    """
    pwd = "mypassword"
    h1 = hash_password(pwd)
    h2 = hash_password(pwd)

    assert h1 != h2
    assert h1 != pwd
    assert h2 != pwd


# ------------------ verify_password ------------------ #

def test_verify_password_correct():
    """
    Коректний пароль має валідуватися успішно.
    """
    pwd = "validpass"
    hashed = hash_password(pwd)

    assert verify_password(pwd, hashed) is True


def test_verify_password_incorrect():
    """
    Невірний пароль має повертати False.
    """
    hashed = hash_password("correctpass")

    assert verify_password("wrongpass", hashed) is False


# ------------------ get_user_by_email ------------------ #

@pytest.mark.asyncio
async def test_get_user_by_email(mock_session):
    """
    Перевіряємо, що get_user_by_email повертає користувача.
    """
    user = User(id=1, email="find@example.com", username="F", password="x")

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user

    mock_session.execute.return_value = mock_result

    result = await get_user_by_email(mock_session, "find@example.com")

    assert result is user
    mock_session.execute.assert_awaited_once()


# ------------------ create_user ------------------ #

@pytest.mark.asyncio
async def test_create_user(mock_session):
    """
    Створює нового користувача та хешує пароль.
    """
    data = UserCreate(
        email="new@example.com",
        username="NewUser",
        password="secret"
    )

    # session.refresh має повернути User
    mock_user = User(id=1, email=data.email, username=data.username, password="hashed")
    mock_session.refresh = AsyncMock(return_value=mock_user)

    result = await create_user(mock_session, data)

    assert isinstance(result, User)
    assert result.email == "new@example.com"
    assert result.username == "NewUser"
    assert result.password != data.password  # пароль має бути хешований

    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called


# ------------------ authenticate_user ------------------ #

@pytest.mark.asyncio
async def test_authenticate_user_success(mock_session):
    """
    Коректний email + пароль → повертає користувача.
    """
    raw_password = "mypassword"
    hashed = hash_password(raw_password)

    user = User(
        id=1,
        email="login@example.com",
        username="Tester",
        password=hashed
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute.return_value = mock_result

    result = await authenticate_user(mock_session, "login@example.com", raw_password)

    assert result is user


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(mock_session):
    """
    Невірний пароль → повертається None.
    """
    user = User(
        id=1,
        email="wrong@example.com",
        username="X",
        password=hash_password("correctpass")
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute.return_value = mock_result

    result = await authenticate_user(mock_session, "wrong@example.com", "wrongpass")

    assert result is None


@pytest.mark.asyncio
async def test_authenticate_user_not_found(mock_session):
    """
    Користувач не існує → повертається None.
    """
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    result = await authenticate_user(mock_session, "nope@example.com", "xxx")

    assert result is None
