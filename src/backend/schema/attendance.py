"Schemas da rota publica /attendance/{ra} (consulta por RA)"
import datetime
from pydantic import BaseModel
from src.backend.database.models import AttendanceStatus


#Uma reunião e o status do aluno nela
class AttendanceItem(BaseModel):

    date: datetime.date
    status: AttendanceStatus


#GET /attendance/{ra}: devolve só o mínimo, sem id, RA ou comitê
class AttendanceLookupResponse(BaseModel):

    name: str
    present: int
    absent: int
    excused: int
    meetings: list[AttendanceItem]
