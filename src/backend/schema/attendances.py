"Schemas da rota /admin/attendances"
from pydantic import BaseModel, ConfigDict
from src.backend.database.models import AttendanceStatus


#POST /admin/attendances
class AttendanceCreate(BaseModel):

    student_id: int
    meeting_id: int
    status: AttendanceStatus


#PUT /admin/attendances/{id}
class AttendanceUpdate(BaseModel):

    status: AttendanceStatus


#GET /admin/attendances, GET /admin/attendances/{id}
class AttendanceResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    meeting_id: int
    status: AttendanceStatus
