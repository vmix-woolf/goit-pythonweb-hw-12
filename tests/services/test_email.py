import pytest
from app.services.email import send_verification_email


@pytest.mark.asyncio
async def test_send_verification_email_prints_link(capfd):
    """
    Перевіряємо, що send_verification_email виводить коректне посилання.
    """
    email = "user@example.com"
    token = "abc123"

    await send_verification_email(email, token)

    captured = capfd.readouterr()
    output = captured.out.strip()

    assert "[DEBUG] Verification link:" in output
    assert "auth/verify?token=abc123" in output
