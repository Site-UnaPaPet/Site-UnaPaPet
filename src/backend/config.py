"Pega as variaveis de ambiente"
from .exceptions import NotFoundEnv
from pathlib import Path 
import os 
from dotenv import load_dotenv
from .logs import logger


class Settings:

    def __init__(self)->None:

        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.DATA = self.BASE_DIR / "data"
        self.DATA.mkdir(exist_ok=True)

        #Variaveis que são obrigatorias
        self.REQUIREDS = ["ORIGIN"]
        self.OPTIONALS = ["URL_DB"]
        self.envs = {}

    #Pega as variaveis obrigatorias
    def _get_requireds_(self) -> None:

        for name in self.REQUIREDS:

            env = os.getenv(name)

            if env is None:
                raise NotFoundEnv(f"Expeted env {name}")

            self.envs[name] = env 

    #Pega os opcionais
    def _get_optionals_(self) -> None:

        for name in self.OPTIONALS:

            self.envs[name] = os.getenv(name)


    #Carrega as variaveis
    def _load(self) -> None:

        path = self.BASE_DIR / ".env"

        load_dotenv(path) if os.path.exists(path) else load_dotenv()

    #chama todos os metodos e retorna as envs
    def get_envs(self) -> dict:

        logger.info("Loading environment...")

        self._load()
        self._get_optionals_()
        self._get_requireds_()

        logger.success("environment loaded successfully")

        


settings = Settings()
settings.get_envs()



    

    

        