"Rotas /admin/attendances"
from fastapi import APIRouter, Depends, HTTPException, status
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import auth_depends, get_ops
from src.backend.schema.attendances import AttendanceCreate, AttendanceUpdate, AttendanceResponse


admin_router = APIRouter(
    prefix="/admin/attendances",
    tags=["admin attendances"],
    dependencies=[Depends(auth_depends.require_admin)],
)


@admin_router.get("", response_model=list[AttendanceResponse])
async def admin_list_attendances(student_id: int | None = None, meeting_id: int | None = None, ops: ManageOperations = Depends(get_ops)):

    if student_id is not None:
        return await ops.list_attendances_by_student(student_id)

    if meeting_id is not None:
        return await ops.list_attendances_by_meeting(meeting_id)

    return await ops.list_attendances()


@admin_router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_attendance(body: AttendanceCreate, ops: ManageOperations = Depends(get_ops)):

    return await ops.create_attendance(**body.model_dump())


@admin_router.get("/{id}", response_model=AttendanceResponse)
async def admin_get_attendance(id: int, ops: ManageOperations = Depends(get_ops)):

    item = await ops.get_attendance(id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")

    return item


@admin_router.put("/{id}", response_model=AttendanceResponse)
async def admin_update_attendance(id: int, body: AttendanceUpdate, ops: ManageOperations = Depends(get_ops)):

    item = await ops.update_attendance_status(id, body.status)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")

    return item


@admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_attendance(id: int, ops: ManageOperations = Depends(get_ops)):

    if not await ops.delete_attendance(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
