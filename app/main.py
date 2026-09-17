from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.connection import create_tables, get_db
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
    except SQLAlchemyError as exc:
        raise RuntimeError("Error al inicializar la base de datos") from exc
    yield


app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios y dispositivos del sistema device_systems. "
        "Incluye operaciones CRUD, validación de datos, manejo de errores "
        "y Dependency Injection."
    ),
    version="2.0.0",
    lifespan=lifespan,
    contact={
        "name": "Esthefany Valentina Chávez Parra",
    },
    openapi_tags=[
        {"name": "Users", "description": "Operaciones CRUD para la gestión de usuarios."},
        {"name": "Devices", "description": "Operaciones CRUD para la gestión de dispositivos."},
        {"name": "Loans", "description": "Operaciones para la gestión de préstamos."},
    ],
)


app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return response


@app.get(
    "/",
    summary="Verificar estado de la API",
    description="Comprueba que la API device_systems se encuentre funcionando.",
    response_description="Mensaje de confirmación",
)
def root():
    return {"message": "device_systems API funcionando"}


@app.get("/test-db/", summary="Verificar conexión con SQLite")
def test_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "conectada"}