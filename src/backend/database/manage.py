"Junta os modulos"
from .connection.manage import ManageConnect
from .migration.migrate import Migrate
from src.backend.config import Settings
from src.backend.database.operations.manage import ManageOperations
class ManageDb:

    def __init__(self)->None:

        instance = Settings(optionals=["URL_DB"])

        self.url = instance.envs.get("URL_DB")
        

    async def migrate(self) -> Migrate:

        conn = ManageConnect(url=self.url, is_async=False)
        await conn.connection()

        return Migrate(engine=conn.engine)

    async def operations(self) -> ManageOperations:

        instance = ManageConnect(url=self.url)
        await instance.connection()

        return ManageOperations(session=instance.session())

    

    