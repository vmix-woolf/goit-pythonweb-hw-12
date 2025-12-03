from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.crud.user import get_user_by_email
from app.database import async_session
from app.models.user import User
from app.schemas.user import TokenData
from app.config import settings

# Секрет і алгоритм JWT
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# OAuth2 схема (точка отримання токена буде /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Створює JWT токен доступу.

    Args:
        data: Дані, які будуть закодовані в токен (наприклад email).
        expires_delta: Час життя токена. Якщо не передано – використовується значення за замовчуванням.

    Returns:
        str: Підписаний JWT токен.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def verify_token(token: str) -> TokenData:
    """
    Перевіряє валідність JWT токена.

    Args:
        token: JWT токен для перевірки.

    Returns:
        TokenData: Об'єкт з email користувача, витягнутим з токена.

    Raises:
        HTTPException: Якщо токен недійсний або протермінований.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise ValueError("Invalid token payload")

        return TokenData(email=email)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Повертає поточного користувача на основі переданого JWT токена.

    Args:
        token: JWT токен із заголовка Authorization.

    Returns:
        User: Поточний користувач, якщо токен валідний.

    Raises:
        HTTPException: Якщо користувача не знайдено або токен недійсний.
    """
    token_data = await verify_token(token)

    async with async_session() as session:
        user = await get_user_by_email(session, token_data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
