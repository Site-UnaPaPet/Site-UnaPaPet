"Schemas da rota /posts e /admin/posts"
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


#POST /admin/posts
class PostCreate(BaseModel):

    title: str = Field(min_length=1, max_length=150)
    published_at: datetime
    summary: str | None = None
    image_url: str | None = Field(default=None, max_length=500)


#PUT /admin/posts/{id}
class PostUpdate(BaseModel):

    title: str | None = Field(default=None, min_length=1, max_length=150)
    published_at: datetime | None = None
    summary: str | None = None
    image_url: str | None = Field(default=None, max_length=500)


#GET /posts, GET /posts/{id}, respostas do /admin/posts
class PostResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: str | None
    image_url: str | None
    published_at: datetime
