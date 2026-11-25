"Schemas da rota /events e /admin/events"
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


#POST /admin/events
class EventCreate(BaseModel):

    title: str = Field(min_length=1, max_length=150)
    starts_at: datetime
    description: str | None = None
    location: str | None = Field(default=None, max_length=150)
    image_url: str | None = Field(default=None, max_length=500)


#PUT /admin/events/{id}
class EventUpdate(BaseModel):

    title: str | None = Field(default=None, min_length=1, max_length=150)
    starts_at: datetime | None = None
    description: str | None = None
    location: str | None = Field(default=None, max_length=150)
    image_url: str | None = Field(default=None, max_length=500)


#GET /events, GET /events/{id}, respostas do /admin/events
class EventResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    location: str | None
    starts_at: datetime
    image_url: str | None
