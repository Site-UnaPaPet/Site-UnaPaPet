"Rotas /admin/meetings"
from fastapi import APIRouter, Depends, HTTPException, status
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import auth_depends, get_ops
from src.backend.schema.meetings import MeetingCreate, MeetingUpdate, MeetingResponse


admin_router = APIRouter(
    prefix="/admin/meetings",
    tags=["admin meetings"],
    dependencies=[Depends(auth_depends.require_admin)],
)


@admin_router.get("", response_model=list[MeetingResponse])
async def admin_list_meetings(ops: ManageOperations = Depends(get_ops)):

    return await ops.list_meetings()


@admin_router.post("", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_meeting(body: MeetingCreate, ops: ManageOperations = Depends(get_ops)):

    return await ops.create_meeting(body.date)


@admin_router.get("/{id}", response_model=MeetingResponse)
async def admin_get_meeting(id: int, ops: ManageOperations = Depends(get_ops)):

    item = await ops.get_meeting(id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

    return item


@admin_router.put("/{id}", response_model=MeetingResponse)
async def admin_update_meeting(id: int, body: MeetingUpdate, ops: ManageOperations = Depends(get_ops)):

    item = await ops.update_meeting(id, body.date)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

    return item


@admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_meeting(id: int, ops: ManageOperations = Depends(get_ops)):

    if not await ops.delete_meeting(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
