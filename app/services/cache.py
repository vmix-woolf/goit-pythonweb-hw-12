import redis.asyncio as redis
import json
from app.config import settings

# Підключення до Redis
redis_client = redis.from_url(settings.redis_url, decode_responses=True)


async def get_cached_user(email: str) -> dict | None:
    """
    Отримує користувача з кешу Redis за email.

    Args:
        email: Email користувача

    Returns:
        dict | None: Дані користувача або None
    """
    try:
        user_data = await redis_client.get(f"user:{email}")
        if user_data:
            return json.loads(user_data)
        return None
    except Exception:
        return None


async def cache_user(email: str, user_data: dict, expire_time: int = 3600):
    """
    Кешує користувача в Redis за email.

    Args:
        email: Email користувача
        user_data: Дані користувача для кешування
        expire_time: Час життя кешу в секундах (за замовчуванням 1 година)
    """
    try:
        await redis_client.setex(
            f"user:{email}",
            expire_time,
            json.dumps(user_data)
        )
    except Exception:
        pass  # Якщо Redis недоступний, просто ігноруємо


async def delete_cached_user(email: str):
    """
    Видаляє користувача з кешу.

    Args:
        email: Email користувача
    """
    try:
        await redis_client.delete(f"user:{email}")
    except Exception:
        pass