import enum
from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, Enum


class AttendanceStatus(str, enum.Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    EXCUSED = "EXCUSED"


class Attendances(Base):

    __tablename__ = "attendances"
    __table_args__ = (UniqueConstraint("student_id", "meeting_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    status: Mapped[AttendanceStatus] = mapped_column(Enum(AttendanceStatus), nullable=False)

    student: Mapped["Students"] = relationship(back_populates="attendances")
    meeting: Mapped["Meetings"] = relationship(back_populates="attendances")
