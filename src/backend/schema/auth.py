"Schemas da rota /auth"
from pydantic import BaseModel, Field

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


#POST /auth/register
class RegisterRequest(BaseModel):

    email: str = Field(max_length=255, pattern=EMAIL_PATTERN)
    #bcrypt só usa os primeiros 72 bytes
    password: str = Field(min_length=8, max_length=72)


#POST /auth/login
class LoginRequest(BaseModel):

    email: str = Field(max_length=255, pattern=EMAIL_PATTERN)
    password: str = Field(min_length=1, max_length=72)


#Resposta do login
class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"


#Resposta do register (nunca devolve a senha nem o hash)
class RegisterResponse(BaseModel):

    id: int
    email: str
