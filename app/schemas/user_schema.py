# schemas/user_schema.py

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class APIResponse(BaseModel):
    status: str
    message: str
    data: dict | None = None
