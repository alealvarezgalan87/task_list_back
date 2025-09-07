from fastapi import HTTPException, status


class TaskListException(HTTPException):
    """Excepción base para la aplicación."""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
    ):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(TaskListException):
    """Excepción para recursos no encontrados."""
    
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedException(TaskListException):
    """Excepción para accesos no autorizados."""
    
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class ForbiddenException(TaskListException):
    """Excepción para accesos prohibidos."""
    
    def __init__(self, detail: str = "Acceso prohibido"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class BadRequestException(TaskListException):
    """Excepción para solicitudes incorrectas."""
    
    def __init__(self, detail: str = "Solicitud incorrecta"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
