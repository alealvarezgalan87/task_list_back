from typing import Generator, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import TokenData

# Configuración de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Obtiene el usuario actual a partir del token JWT.
    
    Args:
        db: Sesión de base de datos.
        token: Token JWT.
        
    Returns:
        El usuario autenticado.
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=UUID(user_id))
    except JWTError:
        raise credentials_exception
    
    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",
        )
    
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Autentica a un usuario por email y contraseña.
    
    Args:
        db: Sesión de base de datos.
        email: Email del usuario.
        password: Contraseña en texto plano.
        
    Returns:
        El usuario autenticado o None si las credenciales son inválidas.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
