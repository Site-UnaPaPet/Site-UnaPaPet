"Rota publica /attendance/{ra} (consulta de presença por RA)"
from fastapi import APIRouter, Depends, HTTPException, status
from src.backend.database.models import AttendanceStatus
from src.backend.database.operations.manage import ManageOperations
from src.backend.depends import get_ops
from src.backend.schema.attendance import AttendanceItem, AttendanceLookupResponse

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.get("/{ra}", response_model=AttendanceLookupResponse)
async def get_attendance_by_ra(ra: str, ops: ManageOperations = Depends(get_ops)):

    student = await ops.get_student_by_ra(ra)

    #mesma resposta para RA inexistente e inativo, sem dar pistas
    if student is None or not student.active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    totals = await ops.count_attendances_by_status(student.id)
    attendances = await ops.list_attendances_by_student(student.id)
    dates = {meeting.id: meeting.date for meeting in await ops.list_meetings()}

    meetings = sorted(
        (AttendanceItem(date=dates[a.meeting_id], status=a.status) for a in attendances if a.meeting_id in dates),
        key=lambda item: item.date,
    )

    return AttendanceLookupResponse(
        name=student.name,
        present=totals[AttendanceStatus.PRESENT],
        absent=totals[AttendanceStatus.ABSENT],
        excused=totals[AttendanceStatus.EXCUSED],
        meetings=meetings,
    )
