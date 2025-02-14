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
    public_id = f"Web16/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, overite=True)
    print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    user = await repositories_users.update_avatar_url(user.email, res_url, db)

    return user
