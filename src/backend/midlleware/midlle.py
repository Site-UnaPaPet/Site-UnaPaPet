"Midlleware"
import math
from datetime import datetime, timezone
from .count import CountThread
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI
from src.backend.logs import logger
from src.backend.config import Settings
from src.backend.exceptions import SettingsValueError
from .routes import PUBLIC_ROUTES


class Midlleware(BaseHTTPMiddleware):

    def __init__(self, app:FastAPI, dispatch = None)->None:
        super().__init__(app, dispatch)

        self.settings = Settings(requireds=["RATE_LIMIT", "GLOBAL_RATE_LIMIT"])

        #RATE_LIMIT: requisições por minuto de cada cliente; GLOBAL_RATE_LIMIT: requisições por minuto de todos juntos
        self.rate_limit = self._get_limit("RATE_LIMIT")
        self.global_rate_limit = self._get_limit("GLOBAL_RATE_LIMIT")

        self.instance = CountThread()

    #Converte a variável de ambiente para um número maior que zero
    def _get_limit(self, name:str) -> int:

        try:

            limit = int(self.settings.envs[name])

        except ValueError:

            raise SettingsValueError(f"{name} must be an integer")

        if limit <= 0:
            raise SettingsValueError(f"{name} must be greater than zero")

        return limit

    #Conta uma requisição na janela da chave; devolve None se passou, ou os segundos até liberar se estourou o limite
    async def _hit(self, key:str, limit:int) -> int|None:

        data = await self.instance.get(key)
        now = datetime.now(timezone.utc)

        if data is not None and data["exp"] > now and data["count"] >= limit:
            return max(1, math.ceil((data["exp"] - now).total_seconds()))

        await self.instance.add(key)

        return None

    #Resposta 429 com o tempo de espera
    def _blocked(self, retry_after:int) -> JSONResponse:

        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"},
            headers={"Retry-After": str(retry_after)},
        )

    #Confere o limite do cliente e depois o global
    async def dispatch(self, request:Request, call_next):

        client = request.client.host if request.client else "unknown"

        #primeiro o do cliente: quem estoura o próprio limite é barrado sem gastar o limite global
        retry_after = await self._hit(f"client:{client}", self.rate_limit)

        if retry_after is not None:

            logger.warning(f"Rate limit exceeded by {client}")

            return self._blocked(retry_after)

        retry_after = await self._hit("global", self.global_rate_limit)

        if retry_after is not None:

            logger.warning("Global rate limit exceeded")

            return self._blocked(retry_after)

        return await call_next(request)


    async def _is_public(self, request:Request) -> str:

        is_public = False

        for value in PUBLIC_ROUTES:

            if value["path"] == request.url.path and value["method"] == request.method:
                is_public = True 
                break 


        return is_public



        



    

