"Rotas /admin/committees"
from fastapi import APIRouter, Depends, HTTPException, status
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import auth_depends, get_ops
from src.backend.schema.committees import CommitteeCreate, CommitteeUpdate, CommitteeResponse


admin_router = APIRouter(
    prefix="/admin/committees",
    tags=["admin committees"],
    dependencies=[Depends(auth_depends.require_admin)],
)


@admin_router.get("", response_model=list[CommitteeResponse])
async def admin_list_committees(ops: ManageOperations = Depends(get_ops)):

    return await ops.list_committees()


@admin_router.post("", response_model=CommitteeResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_committee(body: CommitteeCreate, ops: ManageOperations = Depends(get_ops)):

    return await ops.create_committee(body.name)


@admin_router.get("/{id}", response_model=CommitteeResponse)
async def admin_get_committee(id: int, ops: ManageOperations = Depends(get_ops)):

    item = await ops.get_committee(id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Committee not found")

    return item


@admin_router.put("/{id}", response_model=CommitteeResponse)
async def admin_update_committee(id: int, body: CommitteeUpdate, ops: ManageOperations = Depends(get_ops)):

    item = await ops.update_committee(id, body.name)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Committee not found")

    return item


@admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_committee(id: int, ops: ManageOperations = Depends(get_ops)):

    if not await ops.delete_committee(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Committee not found")
