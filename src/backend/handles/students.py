"Rotas /admin/students"
from fastapi import APIRouter, Depends, HTTPException, status
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import auth_depends, get_ops
from src.backend.schema.students import StudentCreate, StudentUpdate, StudentResponse


admin_router = APIRouter(
    prefix="/admin/students",
    tags=["admin students"],
    dependencies=[Depends(auth_depends.require_admin)],
)


@admin_router.get("", response_model=list[StudentResponse])
async def admin_list_students(committee_id: int | None = None, only_active: bool = False, ops: ManageOperations = Depends(get_ops)):

    return await ops.list_students(committee_id=committee_id, only_active=only_active)


@admin_router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_student(body: StudentCreate, ops: ManageOperations = Depends(get_ops)):

    return await ops.create_student(**body.model_dump())


@admin_router.get("/{id}", response_model=StudentResponse)
async def admin_get_student(id: int, ops: ManageOperations = Depends(get_ops)):

    item = await ops.get_student(id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    return item


@admin_router.put("/{id}", response_model=StudentResponse)
async def admin_update_student(id: int, body: StudentUpdate, ops: ManageOperations = Depends(get_ops)):

    item = await ops.update_student(id, **body.model_dump(exclude_unset=True))

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    return item


@admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_student(id: int, ops: ManageOperations = Depends(get_ops)):

    if not await ops.delete_student(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
