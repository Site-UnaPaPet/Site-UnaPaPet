"Operações da tabela meetings"
import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.logs import logger
from src.backend.exceptions import DatabaseOperationError
from src.backend.database.models import Meetings


class MeetingsOperations:

    def __init__(self, session: AsyncSession) -> None:

        self.session = session

    async def create_meeting(self, date: datetime.date) -> Meetings:

        logger.info(f"Creating meeting {date}...")

        try:

            async with self.session.begin():

                meeting = Meetings(date=date)
                self.session.add(meeting)
                await self.session.flush()

                logger.success(f"Meeting {date} created (id={meeting.id})")
                return meeting

        except Exception as error:

            logger.error(f"create_meeting failed: {error}")
            raise DatabaseOperationError(error) from error

    async def get_meeting(self, meeting_id: int) -> Meetings | None:

        logger.info(f"Getting meeting id={meeting_id}...")

        try:

            async with self.session.begin():

                return await self.session.get(Meetings, meeting_id)

        except Exception as error:

            logger.error(f"get_meeting failed: {error}")
            raise DatabaseOperationError(error) from error

    async def get_meeting_by_date(self, date: datetime.date) -> Meetings | None:

        logger.info(f"Getting meeting {date}...")

        try:

            async with self.session.begin():

                result = await self.session.execute(select(Meetings).where(Meetings.date == date))
                return result.scalar_one_or_none()

        except Exception as error:

            logger.error(f"get_meeting_by_date failed: {error}")
            raise DatabaseOperationError(error) from error

    async def list_meetings(self) -> list[Meetings]:

        logger.info("Listing meetings...")

        try:

            async with self.session.begin():

                result = await self.session.execute(select(Meetings).order_by(Meetings.date))
                return list(result.scalars().all())

        except Exception as error:

            logger.error(f"list_meetings failed: {error}")
            raise DatabaseOperationError(error) from error

    async def update_meeting(self, meeting_id: int, date: datetime.date) -> Meetings | None:

        logger.info(f"Updating meeting id={meeting_id}...")

        try:

            async with self.session.begin():

                meeting = await self.session.get(Meetings, meeting_id)

                if meeting is None:
                    logger.warning(f"Meeting id={meeting_id} not found")
                    return None

                meeting.date = date
                await self.session.flush()

                logger.success(f"Meeting id={meeting_id} updated")
                return meeting

        except Exception as error:

            logger.error(f"update_meeting failed: {error}")
            raise DatabaseOperationError(error) from error

    async def delete_meeting(self, meeting_id: int) -> bool:

        logger.info(f"Deleting meeting id={meeting_id}...")

        try:

            async with self.session.begin():

                meeting = await self.session.get(Meetings, meeting_id)

                if meeting is None:
                    logger.warning(f"Meeting id={meeting_id} not found")
                    return False

                await self.session.delete(meeting)
                await self.session.flush()

                logger.success(f"Meeting id={meeting_id} deleted")
                return True

        except Exception as error:

            logger.error(f"delete_meeting failed: {error}")
            raise DatabaseOperationError(error) from error
