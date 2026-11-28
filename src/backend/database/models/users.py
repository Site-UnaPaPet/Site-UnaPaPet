from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String


class Users(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="admin", nullable=False)
