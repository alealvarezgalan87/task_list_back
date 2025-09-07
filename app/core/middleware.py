import logging
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para registrar información sobre las solicitudes y respuestas."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Registrar la solicitud
        logger.info(
            f"Request: {request.method} {request.url.path} - Client: {request.client.host}"
        )
        
        # Procesar la solicitud
        try:
            response = await call_next(request)
            
            # Registrar la respuesta
            process_time = time.time() - start_time
            logger.info(
                f"Response: {request.method} {request.url.path} - Status: {response.status_code} - "
                f"Process time: {process_time:.4f}s"
            )
            
            return response
        except Exception as e:
            # Registrar la excepción
            process_time = time.time() - start_time
            logger.error(
                f"Error: {request.method} {request.url.path} - Error: {str(e)} - "
                f"Process time: {process_time:.4f}s"
            )
            raise


def setup_middleware(app: FastAPI) -> None:
    """Configura los middlewares para la aplicación."""
    app.add_middleware(LoggingMiddleware)
