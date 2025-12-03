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
    return await create_contact(session, data, user_id=current_user.id)


@router.get("/", response_model=list[ContactOut])
async def list_contacts_api(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_contacts(session, user_id=current_user.id)


@router.get("/{contact_id}", response_model=ContactOut)
async def get_contact_api(
    contact_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
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
    return await search_contacts(
        session, user_id=current_user.id,
        first_name=first_name, last_name=last_name, email=email
    )


@router.get("/birthdays", response_model=list[ContactOut])
async def birthdays_api(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_upcoming_birthdays(session, user_id=current_user.id)
