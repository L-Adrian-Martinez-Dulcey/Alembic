from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.models.device_model import Device
from app.schemas.device_schema import (
	DeviceCreate,
	DevicePatch,
	DeviceResponse,
	DeviceUpdate,
)
from app.services import device_service
from app.schemas.loan_schema import LoanDetailResponse
from app.services import loan_service


router = APIRouter(prefix="/devices", tags=["Devices"])


def get_device_or_404(device_id: int, db: Session) -> Device:
	device = device_service.get_device_by_id(db, device_id)
	if device is None:
		from fastapi import HTTPException

		raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
	return device


@router.get(
	"/",
	response_model=list[DeviceResponse],
	summary="Listar dispositivos",
	description="Lista equipos y permite filtrar por tipo, disponibilidad, marca o texto.",
	response_description="Lista de dispositivos que coincide con los filtros.",
)
def list_devices(
	device_type: str | None = Query(default=None),
	is_available: bool | None = Query(default=None),
	brand: str | None = Query(default=None),
	search: str | None = Query(default=None),
	db: Session = Depends(get_db),
):
	return device_service.get_all_devices(db, device_type, is_available, brand, search)


@router.get(
	"/{device_id}",
	response_model=DeviceResponse,
	summary="Consultar dispositivo",
	description="Obtiene un dispositivo por su identificador.",
	response_description="Datos del dispositivo solicitado.",
)
def get_device(device_id: int, db: Session = Depends(get_db)):
	return get_device_or_404(device_id, db)


@router.get("/{device_id}/loans", response_model=list[LoanDetailResponse], summary="Historial del dispositivo")
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
	get_device_or_404(device_id, db)
	return loan_service.get_loan_details(db, device_id=device_id)


@router.post(
	"/",
	response_model=DeviceResponse,
	status_code=status.HTTP_201_CREATED,
	summary="Crear dispositivo",
	description="Registra un equipo tecnológico disponible para préstamo.",
	response_description="Dispositivo creado correctamente.",
)
def create_device(device_data: DeviceCreate, db: Session = Depends(get_db)):
	return device_service.create_device(db, device_data)


@router.put(
	"/{device_id}",
	response_model=DeviceResponse,
	summary="Actualizar dispositivo",
	description="Reemplaza todos los datos editables de un dispositivo.",
	response_description="Dispositivo actualizado correctamente.",
)
def replace_device(
	device_id: int,
	device_data: DeviceUpdate,
	db: Session = Depends(get_db),
):
	device = get_device_or_404(device_id, db)
	return device_service.update_device(db, device, device_data)


@router.patch(
	"/{device_id}",
	response_model=DeviceResponse,
	summary="Actualizar parcialmente",
	description="Actualiza uno o más campos del dispositivo.",
	response_description="Dispositivo actualizado correctamente.",
)
def update_device(
	device_id: int,
	device_data: DevicePatch,
	db: Session = Depends(get_db),
):
	device = get_device_or_404(device_id, db)
	return device_service.patch_device(db, device, device_data)


@router.delete(
	"/{device_id}",
	status_code=status.HTTP_204_NO_CONTENT,
	summary="Eliminar dispositivo",
	description="Elimina un dispositivo por su identificador.",
	response_description="El dispositivo fue eliminado.",
)
def delete_device(device_id: int, db: Session = Depends(get_db)):
	device = get_device_or_404(device_id, db)
	device_service.delete_device(db, device)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
