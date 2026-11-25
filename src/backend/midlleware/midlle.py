"Midlleware"
from .count import CountThread
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI
from src.backend.logs import logger
from src.backend.config import Settings
from .routes import PUBLIC_ROUTES
class Midlleware(BaseHTTPMiddleware):

    def __init__(self, app:FastAPI, dispatch = None)->None:
        super().__init__(app, dispatch)

        self.settings = Settings(requireds=["RATE_LIMIT", "GLOBAL_RATE_LIMIT"])
        self.instance = CountThread()



    async def _is_public(self, request:Request) -> str:

        is_public = False

        for value in PUBLIC_ROUTES:

            if value["path"] == request.url.path and value["method"] == request.method:
                is_public = True 
                break 


        return is_public



        



    

