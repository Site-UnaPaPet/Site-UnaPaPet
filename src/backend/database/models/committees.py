from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String


class Committees(Base):

    __tablename__ = "committees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    students: Mapped[list["Students"]] = relationship(back_populates="committee")
