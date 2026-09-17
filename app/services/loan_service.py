from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, contains_eager

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate, LoanStatus


def get_loan_by_id(db: Session, loan_id: int) -> Loan | None:
	return db.get(Loan, loan_id)


def _loan_details_statement(
	status_filter: LoanStatus | None = None,
	user_email: str | None = None,
	device_type: str | None = None,
	user_id: int | None = None,
	device_id: int | None = None,
):
	conditions = []
	if status_filter is not None:
		conditions.append(Loan.status == status_filter)
	if user_email is not None:
		conditions.append(User.email.ilike(f"%{user_email}%"))
	if device_type is not None:
		conditions.append(Device.device_type.ilike(f"%{device_type}%"))
	if user_id is not None:
		conditions.append(User.id == user_id)
	if device_id is not None:
		conditions.append(Device.id == device_id)

	statement = (
		select(Loan)
		.join(User, Loan.user_id == User.id)
		.join(Device, Loan.device_id == Device.id)
		.options(contains_eager(Loan.user), contains_eager(Loan.device))
		.order_by(Loan.loan_date.desc())
	)
	if conditions:
		statement = statement.where(and_(*conditions))
	return statement


def get_loan_details(
	db: Session,
	status_filter: LoanStatus | None = None,
	user_email: str | None = None,
	device_type: str | None = None,
	user_id: int | None = None,
	device_id: int | None = None,
) -> list[Loan]:
	return list(db.scalars(_loan_details_statement(
		status_filter, user_email, device_type, user_id, device_id
	)).unique().all())


def get_all_loans(db: Session, status_filter: LoanStatus | None = None,
	user_email: str | None = None, device_type: str | None = None) -> list[Loan]:
	return get_loan_details(db, status_filter, user_email, device_type)


def create_loan(db: Session, loan_data: LoanCreate) -> Loan:
	user = db.get(User, loan_data.user_id)
	if user is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Usuario no encontrado",
		)

	device = db.get(Device, loan_data.device_id)
	if device is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Dispositivo no encontrado",
		)
	if not device.is_available:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="El dispositivo no está disponible",
		)

	loan = Loan(
		user_id=user.id,
		device_id=device.id,
		status="active",
	)
	device.is_available = False
	db.add(loan)
	db.commit()
	db.refresh(loan)
	return loan


def return_loan(db: Session, loan: Loan) -> Loan:
	if loan.status == "returned":
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="El préstamo ya fue devuelto",
		)

	device = db.get(Device, loan.device_id)
	if device is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Dispositivo asociado no encontrado",
		)

	loan.status = "returned"
	loan.return_date = datetime.utcnow()
	device.is_available = True
	db.commit()
	db.refresh(loan)
	return loan
