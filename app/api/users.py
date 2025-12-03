from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary.uploader

from app.database import get_session
from app.services.auth import get_current_user
from app.models.user import User
from app.services.avatar import upload_avatar as upload_avatar_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Завантажує новий аватар користувача до Cloudinary та оновлює його профіль.

    Args:
        file: Завантажений файл аватара.
        session: Асинхронна сесія бази даних.
        current_user: Авторизований користувач.

    Returns:
        dict: URL завантаженого аватара.

    Raises:
        HTTPException: Якщо сталася помилка під час завантаження.
    """
    try:
        avatar_url = await upload_avatar_service(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {e}")

    # Синхронізація екземпляра користувача із поточною сесією
    db_user = await session.merge(current_user)

    # Оновлення URL аватара
    db_user.avatar_url = avatar_url
    await session.commit()
    await session.refresh(db_user)

    return {"avatar_url": avatar_url}
