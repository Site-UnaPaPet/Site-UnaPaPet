"Cria e le tokens"
from src.backend.logs import logger
from src.backend.exceptions import InvalidTokenError
import jwt

class JWT:
    def __init__(self, secret:str)->None:

        self.secret = secret
        self.alg = "HS256"

    #Gera o token a partir do payload
    def create(self, payload:dict) -> str:

        logger.info("Creating token...")

        try:

            token = jwt.encode(payload, self.secret, algorithm=self.alg)

            logger.success("Token created")

            return token

        except Exception as error:

            logger.error(f"Failed to create token (invalid secret?): {error}")

            raise InvalidTokenError(error) from error

    #Le o token e devolve o payload
    def read(self, token:str) -> dict:

        logger.info("Reading token...")

        try:

            payload = jwt.decode(token, self.secret, algorithms=[self.alg])

            logger.success("Token read")

            return payload

        except Exception as error:

            logger.error(f"Failed to read token: {error}")

            raise InvalidTokenError(error) from error
