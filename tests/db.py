import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.models.base import Base

POSTGRES_TEST_USER = os.getenv("POSTGRES_TEST_USER")
POSTGRES_TEST_PASSWORD = os.getenv("POSTGRES_TEST_PASSWORD")
POSTGRES_TEST_DB = os.getenv("POSTGRES_TEST_DB")

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_TEST_USER}:"
    f"{POSTGRES_TEST_PASSWORD}@localhost:5433/{POSTGRES_TEST_DB}"
)

# Создаем движок для тестов с pool_pre_ping для стабильности
engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300
)

SessionTest = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


async def override_get_session():
    """Override функция для dependency injection в тестах."""
    async with SessionTest() as session:
        yield session


async def init_test_db():
    """Инициализация тестовой БД - создание таблиц."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)