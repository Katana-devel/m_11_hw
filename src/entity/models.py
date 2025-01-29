from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Date, Integer, Column


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    surname: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)  # Используем mapped_column
    extra_info: Mapped[str] = mapped_column(String(500), nullable=True)
