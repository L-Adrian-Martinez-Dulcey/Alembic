from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceUpdate


def get_device_by_id(db: Session, device_id: int) -> Device | None:
	return db.get(Device, device_id)


def get_all_devices(
	db: Session,
	device_type: str | None = None,
	is_available: bool | None = None,
	brand: str | None = None,
	search: str | None = None,
) -> list[Device]:
	statement = select(Device).order_by(Device.name.asc())
	if device_type is not None:
		statement = statement.where(Device.device_type == device_type)
	if is_available is not None:
		statement = statement.where(Device.is_available == is_available)
	if brand is not None:
		statement = statement.where(Device.brand.ilike(brand))
	if search is not None:
		pattern = f"%{search}%"
		statement = statement.where(
			or_(
				Device.name.ilike(pattern),
				Device.serial_number.ilike(pattern),
				Device.device_type.ilike(pattern),
				Device.brand.ilike(pattern),
			)
		)
	return list(db.scalars(statement).all())


def create_device(db: Session, device_data: DeviceCreate) -> Device:
	device = Device(**device_data.model_dump())
	db.add(device)
	_commit_device(db, device)
	return device


def update_device(db: Session, device: Device, device_data: DeviceUpdate) -> Device:
	for field, value in device_data.model_dump().items():
		setattr(device, field, value)
	_commit_device(db, device)
	return device


def patch_device(db: Session, device: Device, device_data: DevicePatch) -> Device:
	changes = device_data.model_dump(exclude_unset=True)
	if not changes:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Debe enviar al menos un campo para actualizar",
		)
	for field, value in changes.items():
		setattr(device, field, value)
	_commit_device(db, device)
	return device


def delete_device(db: Session, device: Device) -> None:
	db.delete(device)
	db.commit()


def _commit_device(db: Session, device: Device) -> None:
	try:
		db.commit()
	except IntegrityError as exc:
		db.rollback()
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="El número de serie ya está registrado",
		) from exc
	db.refresh(device)
