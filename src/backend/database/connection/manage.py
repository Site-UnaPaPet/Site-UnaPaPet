"Junta os modulos de conexão"
from .engine import Engine, AsyncEngine, EngineDb
from .session import create_session_make, AsyncSession
from src.backend.database.url import get_url

class ManageConnect(EngineDb):

    def __init__(self, url, is_async:bool = True)->None:

        self.url = get_url(url=url)

        super().__init__(self.url, is_async)

        self.engine:Engine|AsyncEngine=self.get_engine()
        self.session:None|AsyncSession=None if not is_async else create_session_make(engine=self.engine)


