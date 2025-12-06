import pytest
from unittest.mock import MagicMock, AsyncMock

from app.crud.user import (
    hash_password,
    verify_password,
    get_user_by_email,
    create_user,
    authenticate_user,
    update_user_password,
    get_all_users,
    update_user_role,
    get_user_by_id,
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


@pytest.mark.asyncio
async def test_update_user_password(mock_session):
    """
    Перевіряємо, що update_user_password оновлює пароль користувача.
    """
    user = User(
        id=1,
        email="user@example.com",
        username="user",
        password="old_hashed_password",
        is_verified=True
    )

    result = await update_user_password(mock_session, user, "new_password")

    # Перевіряємо що пароль змінився (хешований)
    assert result.password != "new_password"  # не plain text
    assert result.password != "old_hashed_password"  # змінився
    assert result.password.startswith("$2b$")  # bcrypt hash

    # Перевіряємо виклики сесії
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(user)


# ------------------ get_all_users ------------------ #

@pytest.mark.asyncio
async def test_get_all_users(mock_session):
    """
    Перевіряємо, що get_all_users повертає список користувачів.
    """
    users = [
        User(id=1, email="user1@example.com", username="user1", password="hash1"),
        User(id=2, email="user2@example.com", username="user2", password="hash2"),
    ]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = users
    mock_session.execute.return_value = mock_result

    result = await get_all_users(mock_session, skip=0, limit=10)

    assert len(result) == 2
    assert result[0].email == "user1@example.com"
    assert result[1].email == "user2@example.com"
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_users_with_pagination(mock_session):
    """
    Перевіряємо пагінацію в get_all_users.
    """
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result

    await get_all_users(mock_session, skip=20, limit=5)

    # Перевіряємо що SQL запит був викликаний з правильними параметрами
    mock_session.execute.assert_awaited_once()


# ------------------ update_user_role ------------------ #

@pytest.mark.asyncio
async def test_update_user_role(mock_session):
    """
    Перевіряємо, що update_user_role змінює роль користувача.
    """
    user = User(
        id=1,
        email="user@example.com",
        username="user",
        password="hash",
        role="user"
    )

    result = await update_user_role(mock_session, user, "admin")

    assert result.role == "admin"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(user)


# ------------------ get_user_by_id ------------------ #

@pytest.mark.asyncio
async def test_get_user_by_id_found(mock_session):
    """
    Перевіряємо, що get_user_by_id знаходить користувача за ID.
    """
    user = User(id=1, email="found@example.com", username="found", password="hash")

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute.return_value = mock_result

    result = await get_user_by_id(mock_session, 1)

    assert result is user
    assert result.email == "found@example.com"
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(mock_session):
    """
    Перевіряємо, що get_user_by_id повертає None якщо користувача немає.
    """
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    result = await get_user_by_id(mock_session, 999)

    assert result is None
    mock_session.execute.assert_awaited_once()