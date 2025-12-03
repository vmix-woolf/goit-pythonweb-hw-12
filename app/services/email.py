from app.config import settings


async def send_verification_email(email: str, token: str) -> None:
    """
    Фейк-надсилання листа.
    Просто виводимо посилання у лог і нічого не шлемо.
    """

    verify_url = f"{settings.app_url}/auth/verify?token={token}"
    print(f"[DEBUG] Verification link: {verify_url}")

    return
