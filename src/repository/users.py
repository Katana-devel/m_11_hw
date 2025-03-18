from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from src.database.fu_db import get_db
from src.entity.models import User

async def get_user_by_email(email, db: AsyncSession = Depends(get_db)):
    """
        Retrieves a user from the database based on their email address.

        Args:
            email (str): Email address of the user.
            db (AsyncSession): Database session used for the query.

        Returns:
            User | None: User object if found, or None if no user matches the email.

    """

    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user

async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> None:
    """
    Updates the avatar URL for a user identified by their email.

    The function retrieves the user, updates their avatar field with the provided URL,
    commits the changes, and refreshes the user object to reflect the new state.

    Args:
        email (str): Email address of the user whose avatar is being updated.
        url (str | None): New avatar URL or None to remove the avatar.
        db (AsyncSession): Database session used to commit the change.

    Returns:
        User: The updated user object with the new avatar URL.

    """

    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user