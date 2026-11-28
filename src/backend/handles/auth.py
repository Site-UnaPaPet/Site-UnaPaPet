"Rotas /auth (register, login, refresh e logout)"
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from src.backend.config import Settings
from src.backend.database.models import Users
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import auth_depends, get_ops
from src.backend.exceptions import InvalidTokenError
from src.backend.logs import logger
from src.backend.schema.auth import LoginRequest, RegisterRequest, RegisterResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

auth = auth_depends.auth

ACCESS_MINUTES = 15
REFRESH_DAYS = 7

#os dois tokens ficam em cookies httpOnly: o access vale para o site todo, o refresh só para /auth
ACCESS_COOKIE = "access_token"
ACCESS_COOKIE_PATH = "/"
REFRESH_COOKIE = "refresh_token"
COOKIE_PATH = "/auth"

#COOKIE_SECURE=false só para desenvolvimento em http
COOKIE_SECURE = (Settings(optionals=["COOKIE_SECURE"]).envs.get("COOKIE_SECURE") or "true").lower() != "false"

#hash falso para gastar o mesmo tempo quando o e-mail não existe (evita descobrir e-mails pelo tempo da resposta)
DUMMY_HASH = auth.generate("senha-falsa")


def _create_access(user: Users) -> str:

    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_MINUTES)

    return auth.create({"sub": str(user.id), "role": user.role, "type": "access", "exp": exp})


def _create_refresh(user: Users) -> str:

    exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_DAYS)

    return auth.create({"sub": str(user.id), "type": "refresh", "exp": exp})


#salva o access e o refresh token em cookies httpOnly (o JavaScript do site não consegue ler) e devolve o access token
def set_cookies(response: Response, user: Users) -> str:

    access = _create_access(user)

    response.set_cookie(
        key=ACCESS_COOKIE,
        value=access,
        max_age=ACCESS_MINUTES * 60,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path=ACCESS_COOKIE_PATH,
    )

    response.set_cookie(
        key=REFRESH_COOKIE,
        value=_create_refresh(user),
        max_age=REFRESH_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path=COOKIE_PATH,
    )

    return access


def clear_cookies(response: Response) -> None:

    response.delete_cookie(key=ACCESS_COOKIE, path=ACCESS_COOKIE_PATH, httponly=True, secure=COOKIE_SECURE, samesite="lax")
    response.delete_cookie(key=REFRESH_COOKIE, path=COOKIE_PATH, httponly=True, secure=COOKIE_SECURE, samesite="lax")


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, response: Response, ops: ManageOperations = Depends(get_ops)):

    if await ops.get_user_by_email(body.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    #a senha nunca vai pro banco em texto puro: só o hash bcrypt; o role é sempre "member"
    user = await ops.create_user(body.email, auth.generate(body.password), role="member")

    access = set_cookies(response, user)

    logger.success(f"User {user.id} registered")

    return RegisterResponse(id=user.id, email=user.email, access_token=access)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, response: Response, ops: ManageOperations = Depends(get_ops)):

    user = await ops.get_user_by_email(body.email)

    valid = auth.compare(body.password, user.password_hash if user is not None else DUMMY_HASH)

    #mesma resposta para e-mail inexistente e senha errada
    if user is None or not valid:

        logger.warning("Failed login")

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access = set_cookies(response, user)

    logger.success(f"User {user.id} logged in")

    return TokenResponse(access_token=access)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    ops: ManageOperations = Depends(get_ops),
):

    invalid = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    if refresh_token is None:
        raise invalid

    try:

        payload = auth.read(refresh_token)

    except InvalidTokenError:

        clear_cookies(response)
        raise invalid

    #o access token não serve como refresh token
    if payload.get("type") != "refresh":
        raise invalid

    user = await ops.get_user(int(payload["sub"]))

    if user is None:

        clear_cookies(response)
        raise invalid

    #gira os dois tokens: a cada uso saem novos
    access = set_cookies(response, user)

    logger.success(f"Token refreshed for user {user.id}")

    return TokenResponse(access_token=access)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):

    clear_cookies(response)

    logger.success("Logged out")
