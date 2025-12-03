import cloudinary
import cloudinary.uploader
from app.config import settings

# Налаштування Cloudinary при старті застосунку
cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)


async def upload_avatar(file):
    """
    Завантажує файл аватара в Cloudinary.

    Args:
        file: Файл, отриманий від користувача (UploadFile).

    Returns:
        str: URL завантаженого аватара.
    """
    result = cloudinary.uploader.upload(
        file.file,
        folder="avatars",
        public_id=None,
        overwrite=True,
    )
    return result["secure_url"]
