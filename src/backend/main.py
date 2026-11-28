"Cria o app FastAPI e junta tudo (cors, middleware, rotas e lifespan)"
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.auth.hash import Hash
from src.backend.config import Settings
from src.backend.database.manage import ManageDb
from src.backend.exceptions import DatabaseOperationError, SettingsValueError
from src.backend.handles import (
    admin, attendance, attendances, auth, committees, events, forms, health, meetings, posts, students, users,
    database_error_handler,
)
from src.backend.logs import logger
from src.backend.midlleware.midlle import Midlleware
import asyncio
import sys

#Roda ao ligar e ao desligar a API: cria a ManageOperations e guarda em request.state.operations
@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting API...")

    ops = await ManageDb().operations()

    yield {"operations": ops}

    logger.info("Stopping API...")

    await ops.session.close()
    await ops.session.bind.dispose()


class Server:

    def __init__(self) -> None:

        self.app = FastAPI(lifespan=lifespan)

    #Adiciona o CORS com as origens da variável ORIGIN (separadas por vírgula; * libera todas)
    def add_cors(self) -> None:

        origins = [origin.strip() for origin in Settings(requireds=["ORIGIN"]).envs["ORIGIN"].split(",") if origin.strip()]

        #"*" libera qualquer origem, mas o navegador não aceita "*" junto com credenciais (cookie do refresh token)
        wildcard = "*" in origins

        if not origins:
            raise SettingsValueError("ORIGIN must list at least one origin")

        if wildcard:
            logger.warning("ORIGIN='*': any site can call the API and the refresh cookie will not work cross-origin. Do not use in production")

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"] if wildcard else origins,
            allow_credentials=not wildcard,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["Authorization", "Content-Type"],
        )

        logger.success(f"CORS enabled for {origins}")

    #Adiciona o middleware de rate limit
    def add_midlleware(self) -> None:

        self.app.add_middleware(Midlleware)

    #Adiciona todas as rotas e o tratador de erros do banco
    def add_routes(self) -> None:

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

        for router in routers:
            self.app.include_router(router)

        self.app.add_exception_handler(DatabaseOperationError, database_error_handler)

    #Executa tudo e devolve o app
    def run(self) -> FastAPI:

        #o último middleware adicionado fica por fora: o CORS vai por último para que
        #até a resposta 429 do rate limit leve os cabeçalhos de CORS (senão o navegador mostra erro de CORS)
        self.add_midlleware()
        self.add_cors()
        self.add_routes()

        return self.app


instance = Server()
app = instance.run()

#Comando: cria as tabelas que ainda não existem
def make_migrate() -> None:

    instance = ManageDb()
    migrate = asyncio.run(instance.migrate())
    migrate.create_tables()


#Comando: cria o admin com ADMIN_EMAIL e ADMIN_PASSWORD (obrigatórias). Se ele já existe, não faz nada
def create_admin() -> None:

    envs = Settings(requireds=["ADMIN_EMAIL", "ADMIN_PASSWORD"]).envs
    email, password = envs["ADMIN_EMAIL"].strip(), envs["ADMIN_PASSWORD"]

    if not email:
        raise SettingsValueError("ADMIN_EMAIL must not be empty")

    #o bcrypt só aceita até 72 bytes
    if len(password) < 8 or len(password.encode()) > 72:
        raise SettingsValueError("ADMIN_PASSWORD must have between 8 and 72 bytes")

    async def create() -> None:

        #outra instância do banco, só para este comando
        ops = await ManageDb().operations()

        try:

            user = await ops.get_user_by_email(email)

            if user is not None:

                logger.warning(f"Admin {email} already exists (role={user.role}), nothing to do")
                return

            await ops.create_user(email, Hash().generate(password), "admin")

            logger.success(f"Admin {email} created")

        finally:

            await ops.session.close()
            await ops.session.bind.dispose()

    asyncio.run(create())


COMMANDS = {"make_migrate": make_migrate, "create_admin": create_admin}


if __name__ == "__main__":

    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command not in COMMANDS:

        print(f"Usage: python -m src.backend.main <{'|'.join(COMMANDS)}>")
        sys.exit(1)

    COMMANDS[command]()
