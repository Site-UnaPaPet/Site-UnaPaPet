"Schemas da rota /admin/meetings"
import datetime
from pydantic import BaseModel, ConfigDict


#POST /admin/meetings
class MeetingCreate(BaseModel):

    date: datetime.date


#PUT /admin/meetings/{id}
class MeetingUpdate(BaseModel):

    date: datetime.date


#GET /admin/meetings, GET /admin/meetings/{id}
class MeetingResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime.date
