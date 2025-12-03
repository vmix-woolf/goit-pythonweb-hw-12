from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserOut, UserLogin
from app.services.email import send_verification_email
from app.services.auth import create_access_token, verify_token, get_current_user
from app.crud.user import create_user, get_user_by_email
from app.database import get_session
from app.services.limiter import limiter
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserOut, status_code=201)
async def signup(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """
    Реєструє нового користувача та надсилає лист із підтвердженням email.

    Args:
        user_data: Дані для створення користувача.
        session: Асинхронна сесія БД.

    Returns:
        UserOut: Створений користувач.

    Raises:
        HTTPException: Якщо користувач із таким email вже існує.
    """
    existing = await get_user_by_email(session, str(user_data.email))
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    user = await create_user(session, user_data)
    token = create_access_token({"sub": user.email})

    await send_verification_email(user.email, token)
    return user


@router.post("/login")
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    """
    Авторизація користувача та видача JWT токена.

    Args:
        user_data: Email та пароль користувача.
        session: Асинхронна сесія БД.

    Returns:
        dict: Access token та тип токена.

    Raises:
        HTTPException: Якщо email або пароль некоректні.
    """
    user = await get_user_by_email(session, str(user_data.email))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    from app.crud.user import verify_password
    if not verify_password(user_data.password, user.password):
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


@router.get("/me")
@limiter.limit("5/minute")
async def get_me(request: Request, current_user: User = Depends(get_current_user)):
    """
    Повертає дані поточного автентифікованого користувача.

    Args:
        request: Об’єкт HTTP-запиту.
        current_user: Поточний авторизований користувач.

    Returns:
        User: Модель користувача.
    """
    return current_user
