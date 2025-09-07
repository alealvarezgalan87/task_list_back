import pytest
from fastapi import status

from app.core.security import get_password_hash
from app.models.user import User


def test_register_user(client, db):
    """Test para registrar un nuevo usuario."""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123",
    }
    response = client.post("/api/auth/register", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    
    # Verificar que el usuario se guardó en la base de datos
    user = db.query(User).filter(User.email == user_data["email"]).first()
    assert user is not None
    assert user.username == user_data["username"]


def test_register_user_duplicate_email(client, test_user):
    """Test para verificar que no se puede registrar un usuario con un email duplicado."""
    user_data = {
        "email": test_user.email,  # Email duplicado
        "username": "newuser",
        "password": "password123",
    }
    response = client.post("/api/auth/register", json=user_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email ya está registrado" in response.json()["detail"]


def test_register_user_duplicate_username(client, test_user):
    """Test para verificar que no se puede registrar un usuario con un username duplicado."""
    user_data = {
        "email": "newuser@example.com",
        "username": test_user.username,  # Username duplicado
        "password": "password123",
    }
    response = client.post("/api/auth/register", json=user_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "nombre de usuario ya está registrado" in response.json()["detail"]


def test_login_user(client, test_user):
    """Test para iniciar sesión con un usuario existente."""
    login_data = {
        "username": test_user.email,
        "password": "password123",
    }
    response = client.post("/api/auth/login", data=login_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_invalid_credentials(client, test_user):
    """Test para verificar que no se puede iniciar sesión con credenciales inválidas."""
    login_data = {
        "username": test_user.email,
        "password": "wrongpassword",
    }
    response = client.post("/api/auth/login", data=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Email o contraseña incorrectos" in response.json()["detail"]
