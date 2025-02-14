from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from src.database.fu_db import get_db
from src.entity.models import User

async def get_user_by_email(email, db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user

async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user