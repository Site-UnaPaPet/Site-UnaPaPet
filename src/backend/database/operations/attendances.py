"Operações da tabela attendances"
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.logs import logger
from src.backend.exceptions import DatabaseOperationError
from src.backend.database.models import Attendances, AttendanceStatus


class AttendancesOperations:

    def __init__(self, session: AsyncSession) -> None:

        self.session = session

    async def create_attendance(self, student_id: int, meeting_id: int, status: AttendanceStatus) -> Attendances:

        logger.info(f"Creating attendance student={student_id} meeting={meeting_id}...")

        try:

            async with self.session.begin():

                attendance = Attendances(student_id=student_id, meeting_id=meeting_id, status=status)
                self.session.add(attendance)
                await self.session.flush()

                logger.success(f"Attendance created (id={attendance.id})")
                return attendance

        except Exception as error:

            logger.error(f"create_attendance failed: {error}")
            raise DatabaseOperationError(error) from error

    async def get_attendance(self, attendance_id: int) -> Attendances | None:

        logger.info(f"Getting attendance id={attendance_id}...")

        try:

            async with self.session.begin():

                return await self.session.get(Attendances, attendance_id)

        except Exception as error:

            logger.error(f"get_attendance failed: {error}")
            raise DatabaseOperationError(error) from error

    async def get_attendance_by_student_meeting(self, student_id: int, meeting_id: int) -> Attendances | None:

        logger.info(f"Getting attendance student={student_id} meeting={meeting_id}...")

        try:

            async with self.session.begin():

                result = await self.session.execute(
                    select(Attendances).where(
                        Attendances.student_id == student_id,
                        Attendances.meeting_id == meeting_id,
                    )
                )
                return result.scalar_one_or_none()

        except Exception as error:

            logger.error(f"get_attendance_by_student_meeting failed: {error}")
            raise DatabaseOperationError(error) from error

    async def list_attendances_by_student(self, student_id: int) -> list[Attendances]:

        logger.info(f"Listing attendances of student={student_id}...")

        try:

            async with self.session.begin():

                result = await self.session.execute(
                    select(Attendances).where(Attendances.student_id == student_id)
                )
                return list(result.scalars().all())

        except Exception as error:

            logger.error(f"list_attendances_by_student failed: {error}")
            raise DatabaseOperationError(error) from error

    async def list_attendances_by_meeting(self, meeting_id: int) -> list[Attendances]:

        logger.info(f"Listing attendances of meeting={meeting_id}...")

        try:

            async with self.session.begin():

                result = await self.session.execute(
                    select(Attendances).where(Attendances.meeting_id == meeting_id)
                )
                return list(result.scalars().all())

            #Totais calculados por query (não são armazenados)

        except Exception as error:

            logger.error(f"list_attendances_by_meeting failed: {error}")
            raise DatabaseOperationError(error) from error

    async def count_attendances_by_status(self, student_id: int) -> dict[AttendanceStatus, int]:

        logger.info(f"Counting attendances of student={student_id}...")

        try:

            async with self.session.begin():

                result = await self.session.execute(
                    select(Attendances.status, func.count())
                    .where(Attendances.student_id == student_id)
                    .group_by(Attendances.status)
                )

                totals = {status: 0 for status in AttendanceStatus}
                totals.update({status: total for status, total in result.all()})
                return totals

        except Exception as error:

            logger.error(f"count_attendances_by_status failed: {error}")
            raise DatabaseOperationError(error) from error

    async def update_attendance_status(self, attendance_id: int, status: AttendanceStatus) -> Attendances | None:

        logger.info(f"Updating attendance id={attendance_id}...")

        try:

            async with self.session.begin():

                attendance = await self.session.get(Attendances, attendance_id)

                if attendance is None:
                    logger.warning(f"Attendance id={attendance_id} not found")
                    return None

                attendance.status = status
                await self.session.flush()

                logger.success(f"Attendance id={attendance_id} updated")
                return attendance

        except Exception as error:

            logger.error(f"update_attendance_status failed: {error}")
            raise DatabaseOperationError(error) from error

    async def delete_attendance(self, attendance_id: int) -> bool:

        logger.info(f"Deleting attendance id={attendance_id}...")

        try:

            async with self.session.begin():

                attendance = await self.session.get(Attendances, attendance_id)

                if attendance is None:
                    logger.warning(f"Attendance id={attendance_id} not found")
                    return False

                await self.session.delete(attendance)
                await self.session.flush()

                logger.success(f"Attendance id={attendance_id} deleted")
                return True

        except Exception as error:

            logger.error(f"delete_attendance failed: {error}")
            raise DatabaseOperationError(error) from error
