from app.config import settings


async def send_verification_email(email: str, token: str) -> None:
    """
    Надсилає фейковий лист із посиланням для верифікації.

    Args:
        email: Email отримувача.
        token: Токен, який включається у посилання для підтвердження.

    Notes:
        У навчальних цілях лист фактично не надсилається.
        Посилання виводиться у лог замість реального SMTP-відправлення.
    """
    verify_url = f"{settings.app_url}/auth/verify?token={token}"
    print(f"[DEBUG] Verification link: {verify_url}")

