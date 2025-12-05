from fastapi import HTTPException, status, Depends
from app.models.user import User
from app.services.auth import get_current_user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Перевіряє що користувач є адміністратором.

    Args:
        current_user: Поточний користувач

    Returns:
        User: Користувач з роллю admin

    Raises:
        HTTPException: Якщо користувач не адмін
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def check_admin_or_self(current_user: User, target_user_id: int) -> bool:
    """
    Перевіряє що користувач є адміном або це його власний профіль.

    Args:
        current_user: Поточний користувач
        target_user_id: ID цільового користувача

    Returns:
        bool: True якщо доступ дозволено
    """
    return current_user.role == "admin" or current_user.id == target_user_id


async def require_admin_or_self(
        target_user_id: int,
        current_user: User = Depends(get_current_user)
) -> User:
    """
    Перевіряє що користувач є адміном або редагує свій профіль.

    Args:
        target_user_id: ID цільового користувача
        current_user: Поточний користувач

    Returns:
        User: Поточний користувач якщо доступ дозволено

    Raises:
        HTTPException: Якщо доступ заборонено
    """
    if not check_admin_or_self(current_user, target_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: admin or self access required"
        )
    return current_user