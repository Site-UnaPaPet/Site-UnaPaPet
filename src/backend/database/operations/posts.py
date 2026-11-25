"Operações da tabela posts"
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.logs import logger
from src.backend.database.models import Posts
from datetime import datetime

ALLOWED_FIELDS = ("title", "summary", "image_url", "published_at")


class PostsOperations:

    def __init__(self, session: AsyncSession) -> None:

        self.session = session

    async def create_post(self, title: str, published_at: datetime, summary: str | None = None, image_url: str | None = None) -> Posts:

        logger.info("Creating post...")

        async with self.session.begin():

            obj = Posts(title=title, summary=summary, image_url=image_url, published_at=published_at)
            self.session.add(obj)
            await self.session.flush()

            logger.success(f"Post created (id={obj.id})")
            return obj

    async def get_post(self, post_id: int) -> Posts | None:

        logger.info(f"Getting post id={post_id}...")

        async with self.session.begin():

            return await self.session.get(Posts, post_id)

    async def list_posts(self) -> list[Posts]:

        logger.info("Listing posts...")

        async with self.session.begin():

            result = await self.session.execute(select(Posts).order_by(Posts.published_at.desc()))
            return list(result.scalars().all())

    async def update_post(self, post_id: int, **fields) -> Posts | None:

        logger.info(f"Updating post id={post_id}...")

        async with self.session.begin():

            obj = await self.session.get(Posts, post_id)

            if obj is None:
                logger.warning(f"Post id={post_id} not found")
                return None

            for key, value in fields.items():

                if key not in ALLOWED_FIELDS:
                    raise ValueError(f"Invalid field for post: {key}")

                setattr(obj, key, value)

            await self.session.flush()

            logger.success(f"Post id={post_id} updated")
            return obj

    async def delete_post(self, post_id: int) -> bool:

        logger.info(f"Deleting post id={post_id}...")

        async with self.session.begin():

            obj = await self.session.get(Posts, post_id)

            if obj is None:
                logger.warning(f"Post id={post_id} not found")
                return False

            await self.session.delete(obj)
            await self.session.flush()

            logger.success(f"Post id={post_id} deleted")
            return True
