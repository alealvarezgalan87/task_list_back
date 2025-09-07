import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.database import Base, get_db
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash


# Configuración de la base de datos de prueba
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Crea una base de datos de prueba para cada test.
    """
    # Crear las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear una sesión de prueba
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Eliminar las tablas después de cada test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    Crea un cliente de prueba para la API.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def test_user(db):
    """
    Crea un usuario de prueba.
    """
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password123"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def token_headers(client, test_user):
    """
    Crea los headers con el token de autenticación.
    """
    login_data = {
        "username": test_user.email,
        "password": "password123",
    }
    response = client.post("/api/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
