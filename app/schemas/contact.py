from pydantic import BaseModel, EmailStr
from datetime import date


# Базова схема (спільні поля)
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date | None = None
    additional_info: str | None = None


# Створення контакту
class ContactCreate(ContactBase):
    pass


# Оновлення контакту
class ContactUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    birthday: date | None = None
    additional_info: str | None = None


# Відповідь API
class ContactOut(ContactBase):
    id: int

    class Config:
        from_attributes = True
