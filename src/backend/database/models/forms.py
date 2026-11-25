from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String


class Forms(Base):

    __tablename__ = "forms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    position: Mapped[int] = mapped_column(default=0, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
