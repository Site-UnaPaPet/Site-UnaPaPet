from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

class Commitees(Base):
    __tablename__  = "commitees"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    students: Mapped[list["Students"]] = relationship(back_populates="commitee")