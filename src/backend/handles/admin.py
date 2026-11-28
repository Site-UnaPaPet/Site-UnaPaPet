"Rota /admin (confirma que o token é de admin e devolve quem é)"
from fastapi import APIRouter, Depends
from src.backend.depends import auth_depends

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("")
async def admin_me(payload: dict = Depends(auth_depends.require_admin)):

    return {"id": int(payload["sub"]), "role": payload["role"]}
