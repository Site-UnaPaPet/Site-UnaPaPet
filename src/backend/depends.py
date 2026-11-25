"Dependencias para injetar nas rotas"
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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

    #Valida o JWT do cabeçalho Authorization: Bearer <token> e retorna o payload
    def get_payload(self, credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict:

        if credentials is None:

            logger.warning("Request without token")

            raise _unauthorized("Not authenticated")

        try:

            payload = self.auth.read(credentials.credentials)

        except InvalidTokenError:

            raise _unauthorized("Invalid or expired token")

        #o refresh token não serve como access token
        if payload.get("type") != "access":

            raise _unauthorized("Invalid or expired token")

        return payload


#Pega a ManageOperations que o main guardou em app.state / request.state
def get_ops(request: Request) -> ManageOperations:

    return request.state.operations


auth_depends = AuthDepends()
