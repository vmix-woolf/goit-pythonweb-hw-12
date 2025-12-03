from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate


# Контекст для хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Перевірка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевіряє чи співпадає пароль з хешем."""
    return pwd_context.verify(plain_password, hashed_password)


# Хешування пароля
def hash_password(password: str) -> str:
    """Створює bcrypt-хеш пароля."""
    return pwd_context.hash(password)


# Отримати користувача за email
async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """Повертає користувача за email або None."""
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


# Створити нового користувача
async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    """Створює нового користувача з хешованим паролем."""
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


# Аутентифікація користувача
async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    """Перевіряє email та пароль. Повертає користувача або None."""
    user = await get_user_by_email(session, email)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user
