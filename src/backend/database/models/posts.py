from datetime import datetime
from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Text


class Posts(Base):

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    published_at: Mapped[datetime] = mapped_column(nullable=False)
