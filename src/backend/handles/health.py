"Rota /health (para o Docker, o CI e o monitoramento saberem se a API está de pé)"
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():

    return {"status": "ok"}
