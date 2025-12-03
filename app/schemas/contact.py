from pydantic import BaseModel, EmailStr
from datetime import date


class ContactBase(BaseModel):
    """
    Базова схема контакту з основними полями.
    """
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date | None = None
    additional_info: str | None = None


class ContactCreate(ContactBase):
    """
    Схема для створення нового контакту.
    """
    pass


class ContactUpdate(BaseModel):
    """
    Схема для часткового оновлення контакту.
    """
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    birthday: date | None = None
    additional_info: str | None = None


class ContactOut(ContactBase):
    """
    Схема відповіді API для повернення даних контакту.
    """
    id: int

    class Config:
        from_attributes = True
