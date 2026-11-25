from src.backend.database._base_ import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey

class Students(Base):

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ra: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    commited_id: mapped_column[int] = mapped_column(ForeignKey("commitees.id"))
    commitee: mapped_column("Commitees") = mapped_column(relationship(back_populates="students"))

