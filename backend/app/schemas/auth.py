from typing import Literal

from pydantic import BaseModel, Field


Role = Literal["patient", "physiotherapist", "admin"]


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6)
    role: Role = "patient"


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: Role
    is_active: bool


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse