"Schemas da rota /admin/committees"
from pydantic import BaseModel, ConfigDict, Field


#POST /admin/committees
class CommitteeCreate(BaseModel):

    name: str = Field(min_length=1, max_length=80)


#PUT /admin/committees/{id}
class CommitteeUpdate(BaseModel):

    name: str = Field(min_length=1, max_length=80)


#GET /admin/committees, GET /admin/committees/{id}
class CommitteeResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
