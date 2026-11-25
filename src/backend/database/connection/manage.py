"Junta os modulos de conexão"
from .engine import Engine, AsyncEngine, EngineDb
from .session import create_session_make, AsyncSession
from src.backend.database.url import get_url

class ManageConnect(EngineDb):

    def __init__(self, url:str|None=None, is_async:bool = True)->None:

        self.url = get_url(url=url, is_async=is_async)

        super().__init__(self.url, is_async)

        self.isasync = is_async

        

    async def connection(self) ->None:

        self.engine:Engine|AsyncEngine= await self.get_engine()
        self.session:None|AsyncSession=None if not self.isasync else create_session_make(engine=self.engine)

