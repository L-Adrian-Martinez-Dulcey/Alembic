from typing import Literal

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.user_dependencies import get_user_or_404
from app.models.user_model import User
from app.schemas.user_schema import Role, UserCreate, UserPatch, UserResponse, UserUpdate
from app.services import user_service
from app.schemas.loan_schema import LoanDetailResponse
from app.services import loan_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse], summary="Listar usuarios")
def list_users(
    role: Role | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    sort_by: Literal["name", "created_at"] = Query(default="name"),
    order: Literal["asc", "desc"] = Query(default="asc"),
    db: Session = Depends(get_db),
):
    return user_service.get_all_users(db, role, is_active, sort_by, order)


@router.get("/email/{email}", response_model=UserResponse, summary="Consultar por email")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, email)
    if user is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.get("/{user_id}", response_model=UserResponse, summary="Consultar usuario")
def get_user(user: User = Depends(get_user_or_404)):
    return user


@router.get("/{user_id}/loans", response_model=list[LoanDetailResponse], summary="Préstamos del usuario")
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    get_user_or_404(user_id, db)
    return loan_service.get_loan_details(db, user_id=user_id)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)


@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar usuario")
def replace_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):
    user = get_user_or_404(user_id, db)
    return user_service.update_user(db, user, user_data)


@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar parcialmente")
def update_user(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db),
):
    user = get_user_or_404(user_id, db)
    return user_service.patch_user(db, user, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    user_service.delete_user(db, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
