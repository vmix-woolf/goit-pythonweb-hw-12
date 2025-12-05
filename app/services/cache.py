import redis.asyncio as redis
from app.config import settings

# Підключення до Redis
redis_client = redis.from_url(settings.redis_url, decode_responses=True)


async def get_cached_user(user_id: int) -> dict | None:
    """
    Отримує користувача з кешу Redis.

    Args:
        user_id: ID користувача

    Returns:
        dict | None: Дані користувача або None
    """
    try:
        user_data = await redis_client.get(f"user:{user_id}")
        if user_data:
            import json
            return json.loads(user_data)
        return None
    except Exception:
        return None


async def cache_user(user_id: int, user_data: dict, expire_time: int = 3600):
    """
    Кешує користувача в Redis.

    Args:
        user_id: ID користувача
        user_data: Дані користувача
        expire_time: Час життя кешу в секундах (за замовчуванням 1 година)
    """
    try:
        import json
        await redis_client.setex(
            f"user:{user_id}",
            expire_time,
            json.dumps(user_data)
        )
    except Exception:
        pass  # Якщо Redis недоступний, просто ігноруємо


async def delete_cached_user(user_id: int):
    """
    Видаляє користувача з кешу.

    Args:
        user_id: ID користувача
    """
    try:
        await redis_client.delete(f"user:{user_id}")
    except Exception:
        pass