import cloudinary
import cloudinary.uploader
from app.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)

async def upload_avatar(file):
    """Upload avatar to Cloudinary and return URL."""
    result = cloudinary.uploader.upload(
        file.file,
        folder="avatars",
        public_id=None,
        overwrite=True,
    )
    return result["secure_url"]
