# schemas/user_schema.py

from pydantic import BaseModel, EmailStr
from typing import Any, Optional
from app.models.user_model import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class VerifyOtpRequest(BaseModel):
    user_id: int
    otp: str

class ResendOtpRequest(BaseModel):
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class UserGetSchema(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class APIResponse(BaseModel):
    status: str
    message: str
    data: Any = None
