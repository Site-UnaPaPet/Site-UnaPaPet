"Junta todas as rotas e os tratadores de erro"
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from src.backend.exceptions import DatabaseOperationError
from . import admin, attendance, attendances, auth, committees, events, forms, health, meetings, posts, students, users  # noqa: F401

#Erro de banco: violação de unicidade/chave vira 409, o resto vira 500 sem vazar detalhes
async def database_error_handler(request: Request, exc: DatabaseOperationError) -> JSONResponse:

    if isinstance(exc.__cause__, IntegrityError):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": "Conflict with existing data"})

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Database error"})
