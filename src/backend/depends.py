"Dependencias para injetar nas rotas"
from collections.abc import AsyncIterator
from fastapi import Cookie, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.backend.auth.manage import AuthManage
from src.backend.database.operations.manage import ManageOperations
from src.backend.exceptions import InvalidTokenError
from src.backend.logs import logger

bearer = HTTPBearer(auto_error=False)


def _unauthorized(detail: str) -> HTTPException:

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


class AuthDepends:

    def __init__(self) -> None:

        self.auth = AuthManage()

        #Exige token válido e role admin (criado aqui para poder usar self.get_payload no Depends)
        def require_admin(payload: dict = Depends(self.get_payload)) -> dict:

            if payload.get("role") != "admin":

                logger.warning(f"User {payload.get('sub')} tried to access an admin route")

                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")

            return payload

        self.require_admin = require_admin

    #Valida o JWT e retorna o payload. O token vem do cookie httpOnly "access_token" (navegador)
    #ou do cabeçalho Authorization: Bearer <token> (outros clientes); se vierem os dois, vale o cabeçalho
    def get_payload(
        self,
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
        access_token: str | None = Cookie(default=None),
    ) -> dict:

        token = credentials.credentials if credentials is not None else access_token

        if token is None:

            logger.warning("Request without token")

            raise _unauthorized("Not authenticated")

        try:

            payload = self.auth.read(token)

        except InvalidTokenError:

            raise _unauthorized("Invalid or expired token")

        #o refresh token não serve como access token
        if payload.get("type") != "access":

            raise _unauthorized("Invalid or expired token")

        return payload


#Entrega uma ManageOperations com uma sessão de banco NOVA para cada requisição (fechada no fim).
#A que o main guardou em request.state.operations só empresta a engine: a AsyncSession não aceita uso
#simultâneo, e duas requisições ao mesmo tempo na mesma sessão dão "A transaction is already begun".
async def get_ops(request: Request) -> AsyncIterator[ManageOperations]:

    sessions = getattr(request.app.state, "sessions", None)

    if sessions is None:

        sessions = async_sessionmaker(request.state.operations.session.bind, expire_on_commit=False)
        request.app.state.sessions = sessions

    async with sessions() as session:

        yield ManageOperations(session=session)


auth_depends = AuthDepends()
