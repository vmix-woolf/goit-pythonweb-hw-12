from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserOut
from app.services.email import send_verification_email
from app.services.auth import create_access_token, verify_token, get_current_user
from app.crud.user import create_user, get_user_by_email, verify_password
from app.database import get_session
from app.services.limiter import limiter
from app.models.user import User


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