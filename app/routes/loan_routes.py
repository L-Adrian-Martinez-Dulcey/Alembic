from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanStatus
from app.services import loan_service


router = APIRouter(prefix="/loans", tags=["Loans"])


def get_loan_or_404(loan_id: int, db: Session):
	loan = loan_service.get_loan_by_id(db, loan_id)
	if loan is None:
		raise HTTPException(status_code=404, detail="Préstamo no encontrado")
	return loan


@router.get(
	"/details",
	response_model=list[LoanDetailResponse],
	summary="Consultar detalles de préstamos",
	description="Combina préstamos con usuarios y dispositivos mediante joins y filtros opcionales.",
	response_description="Préstamos con información relacionada.",
	responses={422: {"description": "Filtro inválido."}},
)
def loan_details(
	status_filter: LoanStatus | None = Query(default=None, alias="status"),
	user_email: str | None = None,
	device_type: str | None = None,
	db: Session = Depends(get_db),
):
	return loan_service.get_loan_details(db, status_filter, user_email, device_type)


@router.get(
	"/",
	response_model=list[LoanDetailResponse],
	summary="Listar préstamos",
	description="Lista préstamos y filtra por estado, correo del usuario o tipo de dispositivo.",
	response_description="Lista de préstamos con usuario y dispositivo.",
	responses={422: {"description": "Filtro inválido."}},
)
def list_loans(
	status_filter: LoanStatus | None = Query(default=None, alias="status"),
	user_email: str | None = None,
	device_type: str | None = None,
	db: Session = Depends(get_db),
):
	return loan_service.get_all_loans(db, status_filter, user_email, device_type)


@router.get(
	"/{loan_id}",
	response_model=LoanDetailResponse,
	summary="Consultar préstamo",
	description="Obtiene un préstamo con sus datos relacionados.",
	response_description="Detalle del préstamo solicitado.",
	responses={404: {"description": "Préstamo no encontrado."}},
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
	return get_loan_or_404(loan_id, db)


@router.post(
	"/",
	response_model=LoanDetailResponse,
	status_code=status.HTTP_201_CREATED,
	summary="Crear préstamo",
	description="Presta un dispositivo disponible a un usuario existente.",
	response_description="Préstamo creado y dispositivo marcado como no disponible.",
	responses={
		404: {"description": "Usuario o dispositivo no encontrado."},
		409: {"description": "El dispositivo no está disponible."},
		422: {"description": "Datos de entrada inválidos."},
	},
)
def create_loan(loan_data: LoanCreate, db: Session = Depends(get_db)):
	return loan_service.create_loan(db, loan_data)


@router.patch(
	"/{loan_id}/return",
	response_model=LoanDetailResponse,
	summary="Registrar devolución",
	description="Registra la devolución y vuelve a habilitar el dispositivo.",
	response_description="Préstamo devuelto correctamente.",
	responses={
		404: {"description": "Préstamo o dispositivo no encontrado."},
		409: {"description": "El préstamo ya fue devuelto."},
	},
)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
	loan = get_loan_or_404(loan_id, db)
	return loan_service.return_loan(db, loan)
