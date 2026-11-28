"Schemas da rota /forms e /admin/forms"
from pydantic import BaseModel, ConfigDict, Field


#POST /admin/forms
class FormCreate(BaseModel):

    title: str = Field(min_length=1, max_length=150)
    url: str = Field(min_length=1, max_length=500)
    position: int = 0
    active: bool = True


#PUT /admin/forms/{id}
class FormUpdate(BaseModel):

    title: str | None = Field(default=None, min_length=1, max_length=150)
    url: str | None = Field(default=None, min_length=1, max_length=500)
    position: int | None = None
    active: bool | None = None


#GET /forms, respostas do /admin/forms
class FormResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    url: str
    position: int
    active: bool
