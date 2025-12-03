from pydantic import BaseModel, EmailStr


# Базова схема користувача
class UserBase(BaseModel):
    email: EmailStr


# Схема для створення користувача
class UserCreate(UserBase):
    username: str
    password: str


# Схема для логіну користувача
class UserLogin(UserBase):
    password: str


# Схема для оновлення профілю
class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None


# Схема відповіді (повернення користувача)
class UserOut(UserBase):
    id: int
    username: str
    is_verified: bool

    class Config:
        from_attributes = True


# Схема токена доступу
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str
