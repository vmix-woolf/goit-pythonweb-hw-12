import pytest
from app.crud.user import hash_password, verify_password


def test_hash_password_creates_different_hashes():
    """
    Перевіряємо, що однакові паролі хешуються по-різному (bcrypt salt).
    """
    pwd = "mysecret"
    h1 = hash_password(pwd)
    h2 = hash_password(pwd)

    assert h1 != h2
    assert h1.startswith("$2b$")
    assert h2.startswith("$2b$")


def test_verify_password_correct():
    """
    Перевіряємо, що verify_password підтверджує правильний пароль.
    """
    pwd = "test12345"
    hashed = hash_password(pwd)

    assert verify_password(pwd, hashed) is True


def test_verify_password_incorrect():
    """
    Перевіряємо, що неправильний пароль не проходить перевірку.
    """
    hashed = hash_password("correctpass")

    assert verify_password("wrongpass", hashed) is False
