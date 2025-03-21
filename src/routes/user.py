"""
This module defines API routes related to user operations such as:
- Requesting email confirmation
- Uploading and updating user avatar using Cloudinary
"""

from fastapi import APIRouter,Depends, UploadFile,File, BackgroundTasks, Request


from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary
import cloudinary.uploader
from fastapi_limiter.depends import RateLimiter

from src.database.fu_db import get_db
from src.schemas.user import RequestEmail, UserRead
from src.repository import users as repositories_users
from src.services.email import send_email
from src.entity.models import User
from src.services.auth import current_active_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(get_db)):
    """
    Initiates the email confirmation process for a user.

    - **body**: Contains the email address to confirm.
    - **background_tasks**: Background task handler for sending emails asynchronously.
    - **request**: The incoming HTTP request object (used for building URL).
    - **db**: Asynchronous database session.

    If email already confirmed, returns message; otherwise sends confirmation email.

    """

    user = await repositories_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}


@router.patch(
    "/avatar",
    response_model=UserRead,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def upload_avatar(
        file: UploadFile = File(),
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Uploads and updates the user's avatar image using Cloudinary.

    - **file**: Uploaded image file.
    - **user**: Current authenticated user.
    - **db**: Asynchronous database session.

    Uploads avatar to Cloudinary, updates user's avatar URL in the database,
    and returns the updated user data.
    Rate limited to 1 request per 20 seconds.

    """

    public_id = f"Web16/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, overite=True)
    print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    user = await repositories_users.update_avatar_url(user.email, res_url, db)

    return user
