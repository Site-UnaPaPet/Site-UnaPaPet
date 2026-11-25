"Operações da tabela students"
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.logs import logger
from src.backend.database.models import Students


class StudentsOperations:

    def __init__(self, session: AsyncSession) -> None:

        self.session = session

    async def create_student(self, ra: str, name: str, committee_id: int, active: bool = True) -> Students:

        logger.info(f"Creating student RA={ra}...")

        async with self.session.begin():

            student = Students(ra=ra, name=name, committee_id=committee_id, active=active)
            self.session.add(student)
            await self.session.flush()

            logger.success(f"Student RA={ra} created (id={student.id})")
            return student

    async def get_student(self, student_id: int) -> Students | None:

        logger.info(f"Getting student id={student_id}...")

        async with self.session.begin():

            return await self.session.get(Students, student_id)

    async def get_student_by_ra(self, ra: str) -> Students | None:

        logger.info(f"Getting student RA={ra}...")

        async with self.session.begin():

            result = await self.session.execute(select(Students).where(Students.ra == ra))
            return result.scalar_one_or_none()

    async def list_students(self, committee_id: int | None = None, only_active: bool = False) -> list[Students]:

        logger.info("Listing students...")

        async with self.session.begin():

            query = select(Students).order_by(Students.name)

            if committee_id is not None:
                query = query.where(Students.committee_id == committee_id)

            if only_active:
                query = query.where(Students.active.is_(True))

            result = await self.session.execute(query)
            return list(result.scalars().all())

    async def update_student(self, student_id: int, **fields) -> Students | None:

        logger.info(f"Updating student id={student_id}...")

        async with self.session.begin():

            student = await self.session.get(Students, student_id)

            if student is None:
                logger.warning(f"Student id={student_id} not found")
                return None

            for key, value in fields.items():

                if key not in ("ra", "name", "committee_id", "active"):
                    raise ValueError(f"Invalid field for student: {key}")

                setattr(student, key, value)

            await self.session.flush()

            logger.success(f"Student id={student_id} updated")
            return student

    async def delete_student(self, student_id: int) -> bool:

        logger.info(f"Deleting student id={student_id}...")

        async with self.session.begin():

            student = await self.session.get(Students, student_id)

            if student is None:
                logger.warning(f"Student id={student_id} not found")
                return False

            await self.session.delete(student)
            await self.session.flush()

            logger.success(f"Student id={student_id} deleted")
            return True
