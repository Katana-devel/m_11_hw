"""
This module defines API routes for managing contact information.
Routes include CRUD operations on contacts with rate limiting and user authentication.

"""

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter

from src.database.fu_db import get_db
from src.entity.models import User
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactSchema, ContactResponse, ContactUpdateSchema
from src.services.auth import current_active_user

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    """
    Retrieve a paginated list of contacts belonging to the authenticated user.

    - **limit**: Maximum number of contacts to return (default: 10, min: 10, max: 500).
    - **offset**: Number of contacts to skip from the start (default: 0).
    - **db**: Asynchronous database session.
    - **user**: Current authenticated user.

    Returns a list of contacts.
    Rate limited to 1 request per 20 seconds.

    """

    contacts = await repositories_contacts.get_contacts(limit, offset, db, user)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      user: User = Depends(current_active_user)):
    """
    Retrieve a single contact by its ID for the authenticated user.

    - **contact_id**: ID of the contact to retrieve.
    - **db**: Asynchronous database session.
    - **user**: Current authenticated user.

    Returns the contact if found, else raises 404 error.
    Rate limited to 1 request per 20 seconds.

    """

    contact = await repositories_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                         user: User = Depends(current_active_user)):
    """
    Create a new contact for the authenticated user.

    - **body**: Data for the new contact.
    - **db**: Asynchronous database session.
    - **user**: Current authenticated user.

    Returns the created contact.
    Rate limited to 1 request per 20 seconds.

    """

    contact = await repositories_contacts.create_contacts(body, db, user)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(current_active_user)):
    """
    Update an existing contact for the authenticated user.

    - **contact_id**: ID of the contact to update.
    - **body**: Updated data for the contact.
    - **db**: Asynchronous database session.
    - **user**: Current authenticated user.

    Returns the updated contact if found, else raises 404 error.
    Rate limited to 1 request per 20 seconds.

    """

    contact = await repositories_contacts.update_contacts(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(current_active_user)):
    """
    Delete a contact by its ID for the authenticated user.

    - **contact_id**: ID of the contact to delete.
    - **db**: Asynchronous database session.
    - **user**: Current authenticated user.

    Returns no content if deletion successful, else raises 404 error.
    Rate limited to 1 request per 20 seconds.

    """

    contact = await repositories_contacts.delete_contacts(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
