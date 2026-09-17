from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


Role = Literal["admin", "support", "user"]


class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    email: EmailStr
    role: Role
    is_active: bool = True


class UserCreate(UserBase):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Ana Pérez",
            "email": "ana@sena.edu.co",
            "role": "user",
            "is_active": True,
        }
    })

    pass


class UserUpdate(UserBase):
    pass


class UserPatch(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=120)
    email: EmailStr | None = None
    role: Role | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
