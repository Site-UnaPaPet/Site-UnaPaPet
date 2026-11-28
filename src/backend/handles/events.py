"Rotas /events (publica) e /admin/events"
from fastapi import APIRouter, Depends, HTTPException, status
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import auth_depends, get_ops
from src.backend.schema.events import EventCreate, EventUpdate, EventResponse


router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventResponse])
async def list_events(ops: ManageOperations = Depends(get_ops)):

    return await ops.list_events()


@router.get("/{id}", response_model=EventResponse)
async def get_event(id: int, ops: ManageOperations = Depends(get_ops)):

    event = await ops.get_event(id)

    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return event


admin_router = APIRouter(
    prefix="/admin/events",
    tags=["admin events"],
    dependencies=[Depends(auth_depends.require_admin)],
)


@admin_router.get("", response_model=list[EventResponse])
async def admin_list_events(ops: ManageOperations = Depends(get_ops)):

    return await ops.list_events()


@admin_router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_event(body: EventCreate, ops: ManageOperations = Depends(get_ops)):

    return await ops.create_event(**body.model_dump())


@admin_router.get("/{id}", response_model=EventResponse)
async def admin_get_event(id: int, ops: ManageOperations = Depends(get_ops)):

    item = await ops.get_event(id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return item


@admin_router.put("/{id}", response_model=EventResponse)
async def admin_update_event(id: int, body: EventUpdate, ops: ManageOperations = Depends(get_ops)):

    item = await ops.update_event(id, **body.model_dump(exclude_unset=True))

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return item


@admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_event(id: int, ops: ManageOperations = Depends(get_ops)):

    if not await ops.delete_event(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
