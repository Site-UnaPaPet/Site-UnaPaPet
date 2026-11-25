import datetime
from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Meetings(Base):

    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime.date] = mapped_column(unique=True, nullable=False)

    attendances: Mapped[list["Attendances"]] = relationship(back_populates="meeting")
