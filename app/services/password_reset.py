import secrets
from app.services.cache import redis_client
from app.services.email import send_verification_email


async def create_reset_token(email: str) -> str:
    """
    Створює токен для скидання пароля.

    Args:
        email: Email користувача

    Returns:
        str: Токен для скидання пароля
    """
    # Генеруємо випадковий токен
    token = secrets.token_urlsafe(32)

    # Зберігаємо в Redis на 1 годину
    await redis_client.setex(f"reset:{token}", 3600, email)

    return token


async def verify_reset_token(token: str) -> str | None:
    """
    Перевіряє токен скидання пароля.

    Args:
        token: Токен для перевірки

    Returns:
        str | None: Email користувача або None якщо токен недійсний
    """
    try:
        email = await redis_client.get(f"reset:{token}")
        return email
    except Exception:
        return None


async def delete_reset_token(token: str):
    """
    Видаляє токен після використання.

    Args:
        token: Токен для видалення
    """
    try:
        await redis_client.delete(f"reset:{token}")
    except Exception:
        pass


async def send_password_reset_email(email: str, token: str):
    """
    Надсилає email з посиланням для скидання пароля.

    Args:
        email: Email користувача
        token: Токен для скидання пароля
    """
    # Поки що використовуємо ту ж функцію що і для верифікації
    # В реальному проекті тут має бути окремий шаблон
    print(f"[DEBUG] Password reset link: http://localhost:8000/auth/reset-password?token={token}")

    # Можна викликати send_verification_email або створити окрему функцію
    await send_verification_email(email, token)