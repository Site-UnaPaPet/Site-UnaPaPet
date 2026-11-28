from src.backend.database._base_ import Base
from sqlalchemy import Engine
from src.backend.logs import logger 

class Migrate:

    def __init__(self, engine:Engine)->None:

        self.eng = engine


    #cria as tabelas
    def create_tables(self) -> None:

        logger.info("Creating tables...")

        with self.eng.begin() as session:

            Base.metadata.create_all(session)

        logger.success("Tables created")

    #Deleta as tabelas
    def drop_tables(self) -> None:

        logger.info("Droping tables...")

        with self.eng.begin() as session:

            Base.metadata.drop_all(session)


        logger.success("Droped tables!!")

        

    