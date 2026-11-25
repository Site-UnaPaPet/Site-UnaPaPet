"Operações da tabela users"
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.logs import logger
from src.backend.database.models import Users

ALLOWED_FIELDS = ("email", "password_hash", "role")


class UsersOperations:

    def __init__(self, session: AsyncSession) -> None:

        self.session = session

    async def create_user(self, email: str, password_hash: str, role: str = "admin") -> Users:

        logger.info("Creating user...")

        async with self.session.begin():

            obj = Users(email=email, password_hash=password_hash, role=role)
            self.session.add(obj)
            await self.session.flush()

            logger.success(f"User created (id={obj.id})")
            return obj

    async def get_user(self, user_id: int) -> Users | None:

        logger.info(f"Getting user id={user_id}...")

        async with self.session.begin():

            return await self.session.get(Users, user_id)

    async def list_users(self) -> list[Users]:

        logger.info("Listing users...")

        async with self.session.begin():

            result = await self.session.execute(select(Users).order_by(Users.id))
            return list(result.scalars().all())

    async def update_user(self, user_id: int, **fields) -> Users | None:

        logger.info(f"Updating user id={user_id}...")

        async with self.session.begin():

            obj = await self.session.get(Users, user_id)

            if obj is None:
                logger.warning(f"User id={user_id} not found")
                return None

            for key, value in fields.items():

                if key not in ALLOWED_FIELDS:
                    raise ValueError(f"Invalid field for user: {key}")

                setattr(obj, key, value)

            await self.session.flush()

            logger.success(f"User id={user_id} updated")
            return obj

    async def delete_user(self, user_id: int) -> bool:

        logger.info(f"Deleting user id={user_id}...")

        async with self.session.begin():

            obj = await self.session.get(Users, user_id)

            if obj is None:
                logger.warning(f"User id={user_id} not found")
                return False

            await self.session.delete(obj)
            await self.session.flush()

            logger.success(f"User id={user_id} deleted")
            return True
