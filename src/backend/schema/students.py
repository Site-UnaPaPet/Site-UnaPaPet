"Schemas da rota /admin/students"
from pydantic import BaseModel, ConfigDict, Field


#POST /admin/students
class StudentCreate(BaseModel):

    ra: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=80)
    committee_id: int
    active: bool = True


#PUT /admin/students/{id}
class StudentUpdate(BaseModel):

    ra: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=80)
    committee_id: int | None = None
    active: bool | None = None


#GET /admin/students, GET /admin/students/{id}
class StudentResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    ra: str
    name: str
    committee_id: int
    active: bool
