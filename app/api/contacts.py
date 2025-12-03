from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.contact import (
    create_contact,
    get_contact_by_id,
    get_contacts,
    update_contact,
    delete_contact,
    search_contacts,
    get_upcoming_birthdays,
)
from app.database import get_session
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=ContactOut)
async def create_contact_api(
    data: ContactCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Створює новий контакт для поточного користувача.

    Args:
        data: Дані нового контакту.
        session: Асинхронна сесія бази даних.
        current_user: Авторизований користувач.

    Returns:
        ContactOut: Створений контакт.
    """
    return await create_contact(session, data, user_id=current_user.id)


@router.get("/", response_model=list[ContactOut])
async def list_contacts_api(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає список усіх контактів користувача.

    Args:
        session: Асинхронна сесія бази даних.
        current_user: Авторизований користувач.

    Returns:
        list[ContactOut]: Список контактів.
    """
    return await get_contacts(session, user_id=current_user.id)


@router.get("/{contact_id}", response_model=ContactOut)
async def get_contact_api(
    contact_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає контакт за його ID.

    Args:
        contact_id: Ідентифікатор контакту.
        session: Асинхронна сесія бази даних.
        current_user: Авторизований користувач.

    Returns:
        ContactOut: Контакт, якщо він існує.

    Raises:
        HTTPException: Якщо контакт не знайдено.
    """
    contact = await get_contact_by_id(session, contact_id, user_id=current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactOut)
async def update_contact_api(
    contact_id: int,
    data: ContactUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює дані існуючого контакту.

    Args:
        contact_id: Ідентифікатор контакту.
        data: Нові дані контакту.
        session: Асинхронна сесія бази даних.
        current_user: Авторизований користувач.

    Returns:
        ContactOut: Оновлений контакт.

    Raises:
        HTTPException: Якщо контакт не знайдено.
    """
    contact = await get_contact_by_id(session, contact_id, user_id=current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return await update_contact(session, contact, data)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_api(
    contact_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Видаляє контакт за ID.

    Args:
        contact_id: Ідентифікатор контакту.
        session: Асинхронна сесія бази даних.
        current_user: Авторизований користувач.

    Raises:
        HTTPException: Якщо контакт не знайдено.
    """
    contact = await get_contact_by_id(session, contact_id, user_id=current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    await delete_contact(session, contact)
    return None


@router.get("/search", response_model=list[ContactOut])
async def search_contacts_api(
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Пошук контактів за ім’ям, прізвищем або email.

    Args:
        first_name: Фільтр за ім’ям.
        last_name: Фільтр за прізвищем.
        email: Фільтр за email.
        session: Асинхронна сесія бази даних.
        current_user: Авторизований користувач.

    Returns:
        list[ContactOut]: Список знайдених контактів.
    """
    return await search_contacts(
        session,
        user_id=current_user.id,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )


@router.get("/birthdays", response_model=list[ContactOut])
async def birthdays_api(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає список контактів, у яких день народження незабаром.

    Args:
        session: Асинхронна сесія бази даних.
        current_user: Авторизований користувач.

    Returns:
        list[ContactOut]: Список контактів із близькими днями народження.
    """
    return await get_upcoming_birthdays(session, user_id=current_user.id)
