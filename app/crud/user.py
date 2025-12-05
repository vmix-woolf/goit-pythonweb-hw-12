from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Перевіряє чи відповідає пароль збереженому bcrypt-хешу.
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """
    Створює bcrypt-хеш для нового пароля.
    """
    return pwd_context.hash(password)


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """
    Повертає користувача за email або None, якщо його не існує.
    """
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    """
    Створює нового користувача з хешованим паролем та повертає його.
    """
    hashed_pwd = hash_password(user_data.password)

    new_user = User(
        email=str(user_data.email),
        username=user_data.username,
        password=hashed_pwd,
        is_verified=False,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    """
    Перевіряє email та пароль.
    Повертає користувача, якщо авторизація успішна.
    """
    user = await get_user_by_email(session, email)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


async def update_user_password(session: AsyncSession, user: User, new_password: str) -> User:
    """
    Оновлює пароль користувача.

    Args:
        session: Асинхронна сесія БД.
        user: Користувач для оновлення пароля.
        new_password: Новий пароль.

    Returns:
        User: Оновлений користувач.
    """
    user.password = hash_password(new_password)
    await session.commit()
    await session.refresh(user)
    return user
