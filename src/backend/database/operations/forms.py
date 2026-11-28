"Operações da tabela forms"
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.logs import logger
from src.backend.exceptions import DatabaseOperationError
from src.backend.database.models import Forms

ALLOWED_FIELDS = ("title", "url", "position", "active")


class FormsOperations:

    def __init__(self, session: AsyncSession) -> None:

        self.session = session

    async def create_form(self, title: str, url: str, position: int = 0, active: bool = True) -> Forms:

        logger.info("Creating form...")

        try:

            async with self.session.begin():

                obj = Forms(title=title, url=url, position=position, active=active)
                self.session.add(obj)
                await self.session.flush()

                logger.success(f"Form created (id={obj.id})")
                return obj

        except Exception as error:

            logger.error(f"create_form failed: {error}")
            raise DatabaseOperationError(error) from error

    async def get_form(self, form_id: int) -> Forms | None:

        logger.info(f"Getting form id={form_id}...")

        try:

            async with self.session.begin():

                return await self.session.get(Forms, form_id)

        except Exception as error:

            logger.error(f"get_form failed: {error}")
            raise DatabaseOperationError(error) from error

    async def list_forms(self) -> list[Forms]:

        logger.info("Listing forms...")

        try:

            async with self.session.begin():

                result = await self.session.execute(select(Forms).order_by(Forms.position))
                return list(result.scalars().all())

        except Exception as error:

            logger.error(f"list_forms failed: {error}")
            raise DatabaseOperationError(error) from error

    async def update_form(self, form_id: int, **fields) -> Forms | None:

        logger.info(f"Updating form id={form_id}...")

        try:

            async with self.session.begin():

                obj = await self.session.get(Forms, form_id)

                if obj is None:
                    logger.warning(f"Form id={form_id} not found")
                    return None

                for key, value in fields.items():

                    if key not in ALLOWED_FIELDS:
                        raise ValueError(f"Invalid field for form: {key}")

                    setattr(obj, key, value)

                await self.session.flush()

                logger.success(f"Form id={form_id} updated")
                return obj

        except Exception as error:

            logger.error(f"update_form failed: {error}")
            raise DatabaseOperationError(error) from error

    async def delete_form(self, form_id: int) -> bool:

        logger.info(f"Deleting form id={form_id}...")

        try:

            async with self.session.begin():

                obj = await self.session.get(Forms, form_id)

                if obj is None:
                    logger.warning(f"Form id={form_id} not found")
                    return False

                await self.session.delete(obj)
                await self.session.flush()

                logger.success(f"Form id={form_id} deleted")
                return True

        except Exception as error:

            logger.error(f"delete_form failed: {error}")
            raise DatabaseOperationError(error) from error
