from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.email import send_verification_email
from app.services.auth import create_access_token, verify_token, get_current_user
from app.database import get_session

from app.schemas.user import UserCreate, UserOut, PasswordResetRequest, PasswordReset
from app.services.password_reset import (
    create_reset_token,
    send_password_reset_email,
    verify_reset_token,
    delete_reset_token
)
from app.crud.user import create_user, get_user_by_email, verify_password, update_user_password


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserOut, status_code=201)
async def signup(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await get_user_by_email(session, str(user_data.email))
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    user = await create_user(session, user_data)

    # Для тестів автоматично верифікуємо
    import os
    if os.getenv("TESTING"):
        user.is_verified = True
        await session.commit()

    token = create_access_token({"sub": user.email})
    await send_verification_email(user.email, token)
    return user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    """
    Авторизація користувача та видача JWT токена.

    Args:
        form_data: Email та пароль користувача через OAuth2PasswordRequestForm.
        session: Асинхронна сесія БД.

    Returns:
        dict: Access token та тип токена.

    Raises:
        HTTPException: Якщо email або пароль некоректні.
    """
    user = await get_user_by_email(session, form_data.username)  # username містить email
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify")
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    """
    Підтверджує email користувача на основі токена.

    Args:
        token: Токен підтвердження email.
        session: Асинхронна сесія БД.

    Returns:
        JSONResponse: Повідомлення про успішну верифікацію.

    Raises:
        HTTPException: Якщо користувача не знайдено.
    """
    data = await verify_token(token)

    user = await get_user_by_email(session, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    await session.commit()

    return JSONResponse({"message": "Email successfully verified"})


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    """
    Авторизація користувача та видача JWT токена.

    Args:
        form_data: Email та пароль користувача через OAuth2PasswordRequestForm.
        session: Асинхронна сесія БД.

    Returns:
        dict: Access token та тип токена.

    Raises:
        HTTPException: Якщо email або пароль некоректні.
    """
    user = await get_user_by_email(session, form_data.username)  # username містить email
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Для тестів - автоматично верифікуємо користувача
    import os
    if os.getenv("TESTING"):
        user.is_verified = True
        await session.commit()

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/request-reset")
async def request_password_reset(
        email: str,
        session: AsyncSession = Depends(get_session)
):
    """
    Запитує скидання пароля для користувача.

    Args:
        email: Email користувача для скидання пароля.
        session: Асинхронна сесія БД.

    Returns:
        dict: Повідомлення про успішну відправку.
    """
    # Перевіряємо чи існує користувач
    user = await get_user_by_email(session, email)
    if not user:
        # Не розкриваємо чи існує користувач (безпека)
        return {"message": "If user exists, password reset email has been sent"}

    # Генеруємо токен
    reset_token = await create_reset_token(email)

    # Надсилаємо email
    await send_password_reset_email(email, reset_token)

    return {"message": "Password reset email has been sent"}


@router.post("/request-reset")
async def request_password_reset(
        request: PasswordResetRequest,
        session: AsyncSession = Depends(get_session)
):
    """
    Запитує скидання пароля для користувача.

    Args:
        request: Запит з email користувача для скидання пароля.
        session: Асинхронна сесія БД.

    Returns:
        dict: Повідомлення про успішну відправку.
    """
    # Перевіряємо чи існує користувач
    user = await get_user_by_email(session, str(request.email))
    if not user:
        # Не розкриваємо чи існує користувач (безпека)
        return {"message": "If user exists, password reset email has been sent"}

    # Генеруємо токен
    reset_token = await create_reset_token(str(request.email))

    # Надсилаємо email
    await send_password_reset_email(str(request.email), reset_token)

    return {"message": "Password reset email has been sent"}


@router.post("/reset-password")
async def reset_password(
        request: PasswordReset,
        session: AsyncSession = Depends(get_session)
):
    """
    Скидає пароль користувача за допомогою токена.

    Args:
        request: Токен та новий пароль.
        session: Асинхронна сесія БД.

    Returns:
        dict: Повідомлення про успішне скидання пароля.

    Raises:
        HTTPException: Якщо токен недійсний або користувача не знайдено.
    """
    # Перевіряємо токен
    email = await verify_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    # Знаходимо користувача
    user = await get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Оновлюємо пароль
    await update_user_password(session, user, request.new_password)

    # Видаляємо токен після використання
    await delete_reset_token(request.token)

    # Очищаємо кеш користувача (якщо був кешований)
    from app.services.cache import delete_cached_user
    await delete_cached_user(email)

    return {"message": "Password has been successfully reset"}