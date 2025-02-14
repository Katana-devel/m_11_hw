import uuid

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str
    surname: str


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    surname: str

class RequestEmail(schemas.BaseUserUpdate):
    email: EmailStr