from datetime import datetime
from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Text


class Events(Base):

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(150))
    starts_at: Mapped[datetime] = mapped_column(nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500))
