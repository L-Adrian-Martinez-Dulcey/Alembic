from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return db.scalar(statement)


def email_exists(db: Session, email: str, exclude_id: int | None = None) -> bool:
    statement = select(User).where(User.email == email)
    if exclude_id is not None:
        statement = statement.where(User.id != exclude_id)
    return db.scalar(statement) is not None


def _ensure_email_available(
    db: Session, email: str, exclude_id: int | None = None
) -> None:
    if email_exists(db, email, exclude_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )


def get_all_users(
    db: Session,
    role: str | None = None,
    is_active: bool | None = None,
    sort_by: Literal["name", "created_at"] = "name",
    order: Literal["asc", "desc"] = "asc",
) -> list[User]:
    statement = select(User)
    if role is not None:
        statement = statement.where(User.role == role)
    if is_active is not None:
        statement = statement.where(User.is_active == is_active)

    sort_column = User.name if sort_by == "name" else User.created_at
    statement = statement.order_by(
        sort_column.desc() if order == "desc" else sort_column.asc()
    )
    return list(db.scalars(statement).all())


def create_user(db: Session, user_data: UserCreate) -> User:
    email = str(user_data.email)
    _ensure_email_available(db, email)
    values = user_data.model_dump()
    values["email"] = email
    user = User(**values)
    db.add(user)
    _commit_user(db, user)
    return user


def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
    values = user_data.model_dump()
    email = str(values["email"])
    _ensure_email_available(db, email, user.id)
    values["email"] = email
    for field, value in values.items():
        setattr(user, field, value)
    _commit_user(db, user)
    return user


def patch_user(db: Session, user: User, user_data: UserPatch) -> User:
    changes = user_data.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar",
        )
    if "email" in changes:
        changes["email"] = str(changes["email"])
        _ensure_email_available(db, changes["email"], user.id)
    for field, value in changes.items():
        setattr(user, field, value)
    _commit_user(db, user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def _commit_user(db: Session, user: User) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        ) from exc
    db.refresh(user)
