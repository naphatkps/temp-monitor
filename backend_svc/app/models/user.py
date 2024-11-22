from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from app.models.response import Response

class UserRequest(BaseModel):
    email: EmailStr
    name: str
    city: str
    country: str

class UserBase(UserRequest):
    id: Optional[str] = Field(default=None, alias="_id")

    class Config:
        orm_mode = True

class _UserResponse(UserRequest):
    pass

class UserResponse(Response):
    data: _UserResponse | list[_UserResponse] | dict
    