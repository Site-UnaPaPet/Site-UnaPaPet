from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey


class Students(Base):

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ra: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    committee_id: Mapped[int] = mapped_column(ForeignKey("committees.id"), nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    committee: Mapped["Committees"] = relationship(back_populates="students")
    attendances: Mapped[list["Attendances"]] = relationship(back_populates="student")
