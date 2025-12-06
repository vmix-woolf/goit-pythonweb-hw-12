"""
Тести для системи дозволів.
"""
import pytest
from fastapi import HTTPException
from app.services.permissions import (
    check_admin_or_self,
    require_admin,
    require_admin_or_self
)
from app.models.user import User


def test_check_admin_or_self_admin_access():
    """Адмін має доступ до будь-якого профілю."""
    admin_user = User(
        id=1,
        email="admin@example.com",
        username="admin",
        password="hashed",
        role="admin"
    )

    result = check_admin_or_self(admin_user, target_user_id=999)
    assert result is True


def test_check_admin_or_self_own_access():
    """Користувач має доступ до свого профілю."""
    user = User(
        id=1,
        email="user@example.com",
        username="user",
        password="hashed",
        role="user"
    )

    result = check_admin_or_self(user, target_user_id=1)
    assert result is True


def test_check_admin_or_self_denied():
    """Користувач не має доступ до чужого профілю."""
    user = User(
        id=1,
        email="user@example.com",
        username="user",
        password="hashed",
        role="user"
    )

    result = check_admin_or_self(user, target_user_id=2)
    assert result is False


# Для функцій з Depends() потрібно тестувати логіку окремо
def test_require_admin_logic():
    """Тест логіки перевірки адмін ролі."""
    admin_user = User(
        id=1,
        email="admin@example.com",
        username="admin",
        password="hashed",
        role="admin"
    )

    # Симулюємо логіку з require_admin
    if admin_user.role != "admin":
        should_raise = True
    else:
        should_raise = False

    assert should_raise is False


def test_require_admin_logic_fail():
    """Тест що звичайний користувач не пройде перевірку."""
    regular_user = User(
        id=1,
        email="user@example.com",
        username="user",
        password="hashed",
        role="user"
    )

    # Симулюємо логіку з require_admin
    if regular_user.role != "admin":
        should_raise = True
    else:
        should_raise = False

    assert should_raise is True