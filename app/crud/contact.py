from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


async def get_contacts(session: AsyncSession, user_id: int):
    stmt = select(Contact).where(Contact.owner_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_contact_by_id(session: AsyncSession, contact_id: int, user_id: int):
    stmt = select(Contact).where(
        Contact.id == contact_id,
        Contact.owner_id == user_id
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_contact(session: AsyncSession, data: ContactCreate, user_id: int):
    contact = Contact(
        **data.model_dump(),
        owner_id=user_id,
    )
    session.add(contact)
    await session.commit()
    await session.refresh(contact)
    return contact


async def update_contact(session: AsyncSession, contact: Contact, data: ContactUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)

    await session.commit()
    await session.refresh(contact)
    return contact


async def delete_contact(session: AsyncSession, contact: Contact):
    await session.delete(contact)
    await session.commit()


async def search_contacts(session: AsyncSession, user_id: int,
                          first_name=None, last_name=None, email=None):
    stmt = select(Contact).where(Contact.owner_id == user_id)

    if first_name:
        stmt = stmt.where(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        stmt = stmt.where(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        stmt = stmt.where(Contact.email.ilike(f"%{email}%"))

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_upcoming_birthdays(session: AsyncSession, user_id: int):
    from datetime import date, timedelta

    today = date.today()
    end = today + timedelta(days=7)

    stmt = select(Contact).where(
        Contact.owner_id == user_id,
        Contact.birthday.is_not(None)
    )
    result = await session.execute(stmt)
    contacts = result.scalars().all()

    # фільтруємо в Python за MM-DD
    upcoming = []
    for c in contacts:
        b = c.birthday
        if b and today <= b.replace(year=today.year) <= end:
            upcoming.append(c)

    return upcoming
