from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """
    Базова схема користувача з ключовими полями.
    """
    email: EmailStr


class UserCreate(UserBase):
    """
    Схема для реєстрації нового користувача.
    """
    username: str
    password: str


class UserLogin(UserBase):
    """
    Схема для авторизації користувача.
    """
    password: str


class UserUpdate(BaseModel):
    """
    Схема для оновлення користувача.
    """
    username: str | None = None
    email: EmailStr | None = None
    avatar_url: str | None = None
    role: str | None = None


class UserOut(UserBase):
    """
    Схема виводу користувача.
    """
    id: int
    username: str
    is_verified: bool = False
    avatar_url: str | None = None
    role: str = "user"

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """
    Схема токена доступу, який повертається при вході.
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Дані, витягнуті з JWT токена.
    """
    email: str


class PasswordResetRequest(BaseModel):
    """Схема для запиту скидання пароля."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Схема для скидання пароля."""
    token: str
    new_password: str = Field(min_length=6, max_length=100)