from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact
from src.schemas.contact import ContactSchema, ContactUpdateSchema


# Получить все контакты с пагинацией
async def get_contacts(limit: int, offset: int, db: AsyncSession):
    """
    Retrieves a list of contacts from the database using pagination.

    Args:
        limit (int): Maximum number of contacts to return.
        offset (int): Number of contacts to skip before starting to return results.
        db (AsyncSession): Database session used for the query.

    Returns:
        list[Contact]: List of contact objects from the database

    """

    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


# Получить один контакт по ID
async def get_contact(contact_id: int, db: AsyncSession):
    """
    Retrieves a specific contact from the database by its unique ID.

    Args:
        contact_id (int): Unique identifier of the contact.
        db (AsyncSession): Database session used for the query.

    Returns:
        Contact | None: Contact object if found, or None if no contact matches the ID.

    """

    stmt = select(Contact).filter(Contact.id == contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contacts(body: ContactSchema, db: AsyncSession):
    """
    Creates a new contact record in the database.

    Args:
        body (ContactSchema): Data required to create a new contact, validated via schema.
        db (AsyncSession): Database session used to commit the new contact.

    Returns:
        Contact: The newly created contact object with assigned ID and saved data.

    """

    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contacts(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    """
    Updates an existing contact's information based on the provided ID.

    The function first checks if the contact exists. If it does, it updates each field
    with the provided data and saves the changes to the database.

    Args:
        contact_id (int): ID of the contact to update.
        body (ContactUpdateSchema): Data to update, validated via schema.
        db (AsyncSession): Database session used to commit updates.

    Returns:
        Contact | None: The updated contact object, or None if contact was not found.

    """

    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.extra_info = body.extra_info
        await db.commit()
        await db.refresh(contact)
    return contact

async def delete_contacts(contact_id: int, db: AsyncSession):
    """
    Deletes a contact from the database by its ID.

    The function checks if the contact exists. If found, it deletes the contact
    and commits the changes. If not found, returns None.

    Args:
        contact_id (int): ID of the contact to delete.
        db (AsyncSession): Database session used to perform the deletion.

    Returns:
        Contact | None: The deleted contact object, or None if contact was not found.

    """

    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
