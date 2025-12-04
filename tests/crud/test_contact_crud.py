import pytest
from unittest.mock import AsyncMock, MagicMock

from app.crud.contact import (
    get_contacts,
    get_contact_by_id,
    create_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_upcoming_birthdays,
)
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


# ------------------ get_contacts ------------------ #

@pytest.mark.asyncio
async def test_get_contacts(mock_session):
    mock_contact = Contact(id=1, first_name="A", last_name="B", email="x@x.com", phone="123", owner_id=1)

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_contact]
    mock_session.execute.return_value = mock_result

    contacts = await get_contacts(mock_session, user_id=1)

    assert len(contacts) == 1
    assert contacts[0].id == 1
    mock_session.execute.assert_awaited_once()


# ------------------ get_contact_by_id ------------------ #

@pytest.mark.asyncio
async def test_get_contact_by_id(mock_session):
    mock_contact = Contact(id=10, first_name="A", last_name="B", email="c@c.com", phone="111", owner_id=1)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_contact
    mock_session.execute.return_value = mock_result

    contact = await get_contact_by_id(mock_session, 10, 1)

    assert contact.id == 10
    mock_session.execute.assert_awaited_once()


# ------------------ create_contact ------------------ #

@pytest.mark.asyncio
async def test_create_contact(mock_session):
    data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="jd@example.com",
        phone="12345"
    )

    mock_contact = Contact(id=1, **data.model_dump(), owner_id=1)

    # session.refresh должен вернуть mock_contact
    mock_session.refresh = AsyncMock(return_value=mock_contact)

    result = await create_contact(mock_session, data, user_id=1)

    assert isinstance(result, Contact)
    assert result.first_name == "John"
    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called


# ------------------ update_contact ------------------ #

@pytest.mark.asyncio
async def test_update_contact(mock_session):
    old = Contact(
        id=1,
        first_name="Old",
        last_name="User",
        email="old@example.com",
        phone="123",
        owner_id=1
    )

    data = ContactUpdate(first_name="New")

    result = await update_contact(mock_session, old, data)

    assert result.first_name == "New"
    assert mock_session.commit.called
    assert mock_session.refresh.called


# ------------------ delete_contact ------------------ #

@pytest.mark.asyncio
async def test_delete_contact(mock_session):
    contact = Contact(id=20, first_name="A", last_name="B", email="x", phone="1", owner_id=1)

    await delete_contact(mock_session, contact)

    mock_session.delete.assert_awaited_once_with(contact)
    mock_session.commit.assert_awaited_once()


# ------------------ search_contacts ------------------ #

@pytest.mark.asyncio
async def test_search_contacts(mock_session):
    c = Contact(id=1, first_name="John", last_name="Doe", email="jd@example.com",
                phone="123", owner_id=1)

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [c]
    mock_session.execute.return_value = mock_result

    result = await search_contacts(mock_session, 1, first_name="Jo")

    assert len(result) == 1
    assert result[0].first_name == "John"
    assert mock_session.execute.called


# ------------------ get_upcoming_birthdays ------------------ #

@pytest.mark.asyncio
async def test_get_upcoming_birthdays(mock_session):
    from datetime import date, timedelta

    today = date.today()
    near = today + timedelta(days=3)

    c1 = Contact(
        id=1, first_name="Bob", last_name="R",
        email="a@a.com", phone="1",
        birthday=near,
        owner_id=1
    )
    c2 = Contact(
        id=2, first_name="Tom", last_name="R",
        email="b@b.com", phone="2",
        birthday=today - timedelta(days=10),
        owner_id=1
    )

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [c1, c2]
    mock_session.execute.return_value = mock_result

    result = await get_upcoming_birthdays(mock_session, 1)

    assert len(result) == 1
    assert result[0].id == 1
