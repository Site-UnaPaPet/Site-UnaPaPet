"Rotas /admin/users"
from fastapi import APIRouter, Depends, HTTPException, Response, status
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import auth_depends, get_ops
from src.backend.handles.auth import clear_cookies
from src.backend.schema.users import UserCreate, UserUpdate, UserResponse

admin_router = APIRouter(
    prefix="/admin/users",
    tags=["admin users"],
    dependencies=[Depends(auth_depends.require_admin)],
)


@admin_router.get("", response_model=list[UserResponse])
async def admin_list_users(ops: ManageOperations = Depends(get_ops)):

    return await ops.list_users()


@admin_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_user(body: UserCreate, ops: ManageOperations = Depends(get_ops)):

    if await ops.get_user_by_email(body.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    #a senha nunca vai pro banco em texto puro: só o hash bcrypt
    password_hash = auth_depends.auth.generate(body.password)

    return await ops.create_user(body.email, password_hash, body.role)


@admin_router.get("/{id}", response_model=UserResponse)
async def admin_get_user(id: int, ops: ManageOperations = Depends(get_ops)):

    user = await ops.get_user(id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@admin_router.put("/{id}", response_model=UserResponse)
async def admin_update_user(id: int, body: UserUpdate, ops: ManageOperations = Depends(get_ops)):

    fields = body.model_dump(exclude_unset=True)

    #troca a senha pelo hash antes de salvar
    if fields.get("password") is not None:
        fields["password_hash"] = auth_depends.auth.generate(fields.pop("password"))

    else:
        fields.pop("password", None)

    user = await ops.update_user(id, **fields)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_user(
    id: int,
    response: Response,
    payload: dict = Depends(auth_depends.require_admin),
    ops: ManageOperations = Depends(get_ops),
):

    if not await ops.delete_user(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #se o admin apagou a própria conta, apaga também os cookies de login dele no navegador
    if str(id) == payload["sub"]:
        clear_cookies(response)
