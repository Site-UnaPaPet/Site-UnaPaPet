#junta os modulos
from .hash import Hash
from .token import JWT
from src.backend.config import Settings
class AuthManage(Hash, JWT):

    def __init__(self)->None:

        settings = Settings(requireds=["JWT_SECRET"])
        super().__init__(secret=settings.envs["JWT_SECRET"])