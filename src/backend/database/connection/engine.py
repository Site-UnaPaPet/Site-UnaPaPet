"Cria a engine do banco de dados"
from src.backend.logs import logger 
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import text, create_engine, Engine
from src.backend.exceptions import ConnectionDatabaseError
class EngineDb:

    def __init__(self, url:str, is_async:bool=True)->None:

        self.url = url 
        self.is_async = is_async


    #Cria a engine do banco de dados
    def _create_(self) -> None:

        self.eng = create_async_engine(url=self.url) if self.is_async else create_engine(self.url)

        logger.info("Created engine")

    #Testa a conexão com retry
    async def _test_(self) -> None:

        coutdown = 0

        while True:

            try:

                logger.info("testing database connection...")

                if self.is_async:

                    async with self.eng.begin() as session:

                        await session.execute(
                            text("SELECT 1")
                        )

                else:

                    with self.eng.begin() as session:

                        session.execute(
                            text(
                                "SELECT 1"
                            )
                        )

                logger.success("connection ok!")
                break 

            except Exception as error:

                if coutdown !=3:

                    logger.warning("testing again...")
                    coutdown+=1
                    continue

        
                raise ConnectionDatabaseError(error)

    #Executa todos os metodos e retorna o objeto
    async def get_engine(self) -> AsyncEngine|Engine:

        self._create_()
        await self._test_()
        return self.eng



        