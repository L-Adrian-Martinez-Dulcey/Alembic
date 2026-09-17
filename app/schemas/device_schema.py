from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


DeviceType = Literal[
	"laptop",
	"tablet",
	"proyector",
	"cámara",
	"router",
	"monitor",
]


class DeviceCreate(BaseModel):
	model_config = ConfigDict(json_schema_extra={
		"example": {
			"name": "Laptop Lenovo ThinkPad",
			"serial_number": "LEN-2024-001",
			"device_type": "laptop",
			"brand": "Lenovo",
		}
	})

	name: str = Field(min_length=1, max_length=100)
	serial_number: str = Field(min_length=1, max_length=100)
	device_type: DeviceType
	brand: str | None = Field(default=None, max_length=100)


class DeviceUpdate(DeviceCreate):
	is_available: bool = True


class DevicePatch(BaseModel):
	name: str | None = Field(default=None, min_length=1, max_length=100)
	serial_number: str | None = Field(default=None, min_length=1, max_length=100)
	device_type: DeviceType | None = None
	brand: str | None = Field(default=None, max_length=100)
	is_available: bool | None = None


class DeviceResponse(DeviceCreate):
	model_config = ConfigDict(
		from_attributes=True,
		json_schema_extra={
			"example": {
				"id": 3,
				"name": "Laptop Lenovo ThinkPad",
				"serial_number": "LEN-2024-001",
				"device_type": "laptop",
				"brand": "Lenovo",
				"is_available": True,
				"created_at": "2026-09-17T10:00:00",
			},
		},
	)

	id: int
	is_available: bool
	created_at: datetime
