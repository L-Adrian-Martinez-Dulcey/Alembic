from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database.connection import Base
from app.dependencies.database_dependency import get_db
from app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def override_get_db() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_required_functional_flow(client: TestClient) -> None:
    user_response = client.post(
        "/users/",
        json={
            "name": "Ana Perez",
            "email": "ana@sena.edu.co",
            "role": "user",
        },
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    device_response = client.post(
        "/devices/",
        json={
            "name": "Laptop Lenovo ThinkPad",
            "serial_number": "LEN-2024-001",
            "device_type": "laptop",
            "brand": "Lenovo",
        },
    )
    assert device_response.status_code == 201
    device_id = device_response.json()["id"]

    loan_response = client.post(
        "/loans/",
        json={"user_id": user_id, "device_id": device_id},
    )
    assert loan_response.status_code == 201
    loan_id = loan_response.json()["id"]

    unavailable_response = client.post(
        "/loans/",
        json={"user_id": user_id, "device_id": device_id},
    )
    assert unavailable_response.status_code == 409

    loans_response = client.get("/loans/details")
    assert loans_response.status_code == 200
    assert loans_response.json()[0]["user"]["email"] == "ana@sena.edu.co"
    assert loans_response.json()[0]["device"]["device_type"] == "laptop"

    assert client.get("/loans/?status=active").status_code == 200
    assert client.get("/loans/?device_type=laptop").status_code == 200

    user_loans_response = client.get(f"/users/{user_id}/loans")
    assert user_loans_response.status_code == 200
    assert len(user_loans_response.json()) == 1

    return_response = client.patch(f"/loans/{loan_id}/return")
    assert return_response.status_code == 200
    assert return_response.json()["status"] == "returned"

    device_after_return = client.get(f"/devices/{device_id}")
    assert device_after_return.status_code == 200
    assert device_after_return.json()["is_available"] is True

    device_loans_response = client.get(f"/devices/{device_id}/loans")
    assert device_loans_response.status_code == 200
    assert len(device_loans_response.json()) == 1


def test_invalid_loan_status_returns_422(client: TestClient) -> None:
    response = client.get("/loans/?status=invalid")
    assert response.status_code == 422
