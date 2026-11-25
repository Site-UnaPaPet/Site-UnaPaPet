"Operações da tabela events"
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.logs import logger
from src.backend.exceptions import DatabaseOperationError
from src.backend.database.models import Events
from datetime import datetime

ALLOWED_FIELDS = ("title", "description", "location", "starts_at", "image_url")


class EventsOperations:

    def __init__(self, session: AsyncSession) -> None:

        self.session = session

    async def create_event(self, title: str, starts_at: datetime, description: str | None = None, location: str | None = None, image_url: str | None = None) -> Events:

        logger.info("Creating event...")

        try:

            async with self.session.begin():

                obj = Events(title=title, starts_at=starts_at, description=description, location=location, image_url=image_url)
                self.session.add(obj)
                await self.session.flush()

                logger.success(f"Event created (id={obj.id})")
                return obj

        except Exception as error:

            logger.error(f"create_event failed: {error}")
            raise DatabaseOperationError(error) from error

    async def get_event(self, event_id: int) -> Events | None:

        logger.info(f"Getting event id={event_id}...")

        try:

            async with self.session.begin():

                return await self.session.get(Events, event_id)

        except Exception as error:

            logger.error(f"get_event failed: {error}")
            raise DatabaseOperationError(error) from error

    async def list_events(self) -> list[Events]:

        logger.info("Listing events...")

        try:

            async with self.session.begin():

                result = await self.session.execute(select(Events).order_by(Events.starts_at))
                return list(result.scalars().all())

        except Exception as error:

            logger.error(f"list_events failed: {error}")
            raise DatabaseOperationError(error) from error

    async def update_event(self, event_id: int, **fields) -> Events | None:

        logger.info(f"Updating event id={event_id}...")

        try:

            async with self.session.begin():

                obj = await self.session.get(Events, event_id)

                if obj is None:
                    logger.warning(f"Event id={event_id} not found")
                    return None

                for key, value in fields.items():

                    if key not in ALLOWED_FIELDS:
                        raise ValueError(f"Invalid field for event: {key}")

                    setattr(obj, key, value)

                await self.session.flush()

                logger.success(f"Event id={event_id} updated")
                return obj

        except Exception as error:

            logger.error(f"update_event failed: {error}")
            raise DatabaseOperationError(error) from error

    async def delete_event(self, event_id: int) -> bool:

        logger.info(f"Deleting event id={event_id}...")

        try:

            async with self.session.begin():

                obj = await self.session.get(Events, event_id)

                if obj is None:
                    logger.warning(f"Event id={event_id} not found")
                    return False

                await self.session.delete(obj)
                await self.session.flush()

                logger.success(f"Event id={event_id} deleted")
                return True

        except Exception as error:

            logger.error(f"delete_event failed: {error}")
            raise DatabaseOperationError(error) from error
