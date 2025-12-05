from typing import Sequence
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.auth import get_current_user
from app.models.user import User
from app.services.avatar import upload_avatar as upload_avatar_service
from app.schemas.user import UserOut, UserRoleUpdate
from app.services.permissions import require_admin
from app.crud.user import get_user_by_id, get_all_users, update_user_role
from app.services.cache import delete_cached_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/avatar")
async def upload_avatar(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    """
    Завантажує новий аватар користувача до Cloudinary та оновлює його профіль.
    """
    try:
        avatar_url = await upload_avatar_service(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {e}")

    db_user = await session.merge(current_user)
    db_user.avatar_url = avatar_url
    await session.commit()
    await session.refresh(db_user)

    return {"avatar_url": avatar_url}


@router.get("/me", response_model=UserOut)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Отримує профіль поточного користувача.
    """
    return current_user


@router.get("/", response_model=list[UserOut])
async def get_all_users_admin(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_session),
        admin_user: User = Depends(require_admin)
):
    """
    Отримує список всіх користувачів (тільки для админів).
    """
    users = await get_all_users(session, skip=skip, limit=limit)
    return users


@router.put("/{user_id}/role")
async def update_user_role_admin(
        user_id: int,
        role_data: UserRoleUpdate,
        session: AsyncSession = Depends(get_session),
        admin_user: User = Depends(require_admin)
):
    """
    Оновлює роль користувача (тільки для админів).
    """
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Оновлюємо роль
    updated_user = await update_user_role(session, user, role_data.role)

    # Очищуємо кеш користувача
    await delete_cached_user(user.email)

    return {"message": f"User role updated to {role_data.role}", "user": updated_user}


@router.post("/admin/avatar")
async def upload_default_avatar_admin(
        file: UploadFile = File(...),
        admin_user: User = Depends(require_admin)
):
    """
    Завантажує дефолтний аватар системи (тільки для админів).
    """
    try:
        avatar_url = await upload_avatar_service(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {e}")

    return {
        "message": "Default avatar uploaded successfully",
        "default_avatar_url": avatar_url
    }