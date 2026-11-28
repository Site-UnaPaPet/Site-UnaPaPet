"Schemas da rota /admin/users"
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from .auth import EMAIL_PATTERN

Role = Literal["admin", "member"]


#POST /admin/users (só o admin escolhe o role)
class UserCreate(BaseModel):

    email: str = Field(max_length=255, pattern=EMAIL_PATTERN)
    password: str = Field(min_length=8, max_length=72)
    role: Role = "member"


#PUT /admin/users/{id}
class UserUpdate(BaseModel):

    email: str | None = Field(default=None, max_length=255, pattern=EMAIL_PATTERN)
    password: str | None = Field(default=None, min_length=8, max_length=72)
    role: Role | None = None


#GET /admin/users, GET /admin/users/{id}: sem password_hash
class UserResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: str
