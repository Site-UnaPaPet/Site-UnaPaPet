"Operações da tabela committees"
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.logs import logger
from src.backend.exceptions import DatabaseOperationError
from src.backend.database.models import Committees


class CommitteesOperations:

    def __init__(self, session: AsyncSession) -> None:

        self.session = session

    async def create_committee(self, name: str) -> Committees:

        logger.info(f"Creating committee '{name}'...")

        try:

            async with self.session.begin():

                committee = Committees(name=name)
                self.session.add(committee)
                await self.session.flush()

                logger.success(f"Committee '{name}' created (id={committee.id})")
                return committee

        except Exception as error:

            logger.error(f"create_committee failed: {error}")
            raise DatabaseOperationError(error) from error

    async def get_committee(self, committee_id: int) -> Committees | None:

        logger.info(f"Getting committee id={committee_id}...")

        try:

            async with self.session.begin():

                return await self.session.get(Committees, committee_id)

        except Exception as error:

            logger.error(f"get_committee failed: {error}")
            raise DatabaseOperationError(error) from error

    async def get_committee_by_name(self, name: str) -> Committees | None:

        logger.info(f"Getting committee name='{name}'...")

        try:

            async with self.session.begin():

                result = await self.session.execute(select(Committees).where(Committees.name == name))
                return result.scalar_one_or_none()

        except Exception as error:

            logger.error(f"get_committee_by_name failed: {error}")
            raise DatabaseOperationError(error) from error

    async def list_committees(self) -> list[Committees]:

        logger.info("Listing committees...")

        try:

            async with self.session.begin():

                result = await self.session.execute(select(Committees).order_by(Committees.name))
                return list(result.scalars().all())

        except Exception as error:

            logger.error(f"list_committees failed: {error}")
            raise DatabaseOperationError(error) from error

    async def update_committee(self, committee_id: int, name: str) -> Committees | None:

        logger.info(f"Updating committee id={committee_id}...")

        try:

            async with self.session.begin():

                committee = await self.session.get(Committees, committee_id)

                if committee is None:
                    logger.warning(f"Committee id={committee_id} not found")
                    return None

                committee.name = name
                await self.session.flush()

                logger.success(f"Committee id={committee_id} updated")
                return committee

        except Exception as error:

            logger.error(f"update_committee failed: {error}")
            raise DatabaseOperationError(error) from error

    async def delete_committee(self, committee_id: int) -> bool:

        logger.info(f"Deleting committee id={committee_id}...")

        try:

            async with self.session.begin():

                committee = await self.session.get(Committees, committee_id)

                if committee is None:
                    logger.warning(f"Committee id={committee_id} not found")
                    return False

                await self.session.delete(committee)
                await self.session.flush()

                logger.success(f"Committee id={committee_id} deleted")
                return True

        except Exception as error:

            logger.error(f"delete_committee failed: {error}")
            raise DatabaseOperationError(error) from error
