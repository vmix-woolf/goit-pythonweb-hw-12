import pytest
from unittest.mock import patch, MagicMock

from app.services.avatar import upload_avatar


@pytest.mark.asyncio
async def test_upload_avatar_success(mock_cloudinary_upload):
    """
    Перевіряємо, що upload_avatar повертає URL.
    """

    fake_file = MagicMock()
    fake_file.file = b"fake-bytes"

    url = await upload_avatar(fake_file)

    assert isinstance(url, str)
    assert url.startswith("https://")
    assert url == "https://example.com/avatar.png"
    assert mock_cloudinary_upload.called
