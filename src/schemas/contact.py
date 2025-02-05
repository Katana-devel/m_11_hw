from pydantic import BaseModel, EmailStr, Field
from datetime import date


class ContactSchema(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    surname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=3, max_length=50)
    birthday: date = Field(description="Дата рождения в формате YYYY-MM-DD")
    extra_info: str | None = Field(None, min_length=3, max_length=250)


class ContactUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=50)
    surname: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = Field(None, max_length=255)
    phone: str | None = Field(None, min_length=3, max_length=50)
    birthday: date | None = None
    extra_info: str | None = Field(None, min_length=3, max_length=250)


class ContactResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: date
    extra_info: str | None

    class Config:
        from_attributes = True
