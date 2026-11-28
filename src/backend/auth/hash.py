"Gera e compara hashes de senha"
from src.backend.logs import logger
import bcrypt

class Hash:

    #Gera o hash da senha
    def generate(self, password:str) -> str:

        logger.info("Generating hash...")

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        logger.success("Hash generated")

        return hashed

    #Compara a senha com o hash
    def compare(self, password:str, hashed:str) -> bool:

        logger.info("Comparing hash...")

        try:

            valid = bcrypt.checkpw(password.encode(), hashed.encode())

        except ValueError as error:

            logger.error(f"Failed to compare hash: {error}")

            return False

        if valid:
            logger.success("Hash matches")

        else:
            logger.warning("Hash does not match")

        return valid
