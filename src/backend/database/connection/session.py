#Cria o orquestrador de sessões
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine
from src.backend.logs import logger
from src.backend.exceptions import SessionMakeError


def create_session_make(engine:AsyncEngine) -> AsyncSession:

    try:

        logger.info("Creating session make...")

        session = async_sessionmaker(
            engine, 
            expire_on_commit=False
        )

        logger.success("session make successfully created")

        return session

    except Exception as error:
        raise SessionMakeError(error)



