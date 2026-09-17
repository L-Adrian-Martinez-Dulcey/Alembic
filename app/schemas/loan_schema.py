
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


LoanStatus = Literal["active", "returned", "overdue"]


class LoanCreate(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {"user_id": 1, "device_id": 3, "status": "active"}
    })

    user_id: int
    device_id: int
    status: LoanStatus = "active"


class LoanUpdate(BaseModel):
    return_date: datetime | None = None
    status: LoanStatus


class LoanResponse(LoanCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    loan_date: datetime
    return_date: datetime | None


class UserSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class DeviceSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    serial_number: str
    device_type: str


class LoanDetailResponse(LoanResponse):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "device_id": 3,
                "loan_date": "2026-09-17T10:00:00",
                "return_date": None,
                "status": "active",
                "user": {
                    "id": 1,
                    "name": "Ana Pérez",
                    "email": "ana@sena.edu.co",
                },
                "device": {
                    "id": 3,
                    "name": "Laptop Lenovo ThinkPad",
                    "serial_number": "LEN-2024-001",
                    "device_type": "laptop",
                },
            },
        },
    )

    user: UserSummary
    device: DeviceSummary
