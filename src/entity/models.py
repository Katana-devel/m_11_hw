from datetime import date

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, generics
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, Date, Integer, Column, DateTime, func, ForeignKey


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    surname: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    extra_info: Mapped[str] = mapped_column(String(500), nullable=True)

    user_id: Mapped[int] = mapped_column(generics.GUID(), ForeignKey('user.id'), nullable=True)
    user: Mapped["User"] = relationship("User", backref="contacts", lazy="joined")


class User(SQLAlchemyBaseUserTableUUID, Base):
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    surname: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
