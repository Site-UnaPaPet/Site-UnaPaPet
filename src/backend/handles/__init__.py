"Junta todas as rotas e os tratadores de erro"
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from src.backend.exceptions import DatabaseOperationError
from . import admin, attendance, attendances, auth, committees, events, forms, health, meetings, posts, students, users

routers = [
    health.router,
    auth.router,
    admin.router,
    events.router, events.admin_router,
    posts.router, posts.admin_router,
    forms.router, forms.admin_router,
    attendance.router,
    committees.admin_router,
    students.admin_router,
    meetings.admin_router,
    attendances.admin_router,
    users.admin_router,
]


#Erro de banco: violação de unicidade/chave vira 409, o resto vira 500 sem vazar detalhes
async def database_error_handler(request: Request, exc: DatabaseOperationError) -> JSONResponse:

    if isinstance(exc.__cause__, IntegrityError):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": "Conflict with existing data"})

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Database error"})


def include_routes(app: FastAPI) -> None:

    for router in routers:
        app.include_router(router)

    app.add_exception_handler(DatabaseOperationError, database_error_handler)
