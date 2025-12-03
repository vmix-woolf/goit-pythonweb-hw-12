from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

# Асинхронний двигун для підключення до бази даних
engine = create_async_engine(settings.database_url, echo=False)

# Фабрика для створення асинхронних сесій
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Створює та надає асинхронну сесію бази даних.

    Yields:
        AsyncSession: Активна асинхронна сесія SQLAlchemy.
    """
    async with async_session() as session:
        yield session
