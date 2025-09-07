from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.routes import tasks, auth
from app.core.config import settings
from app.core.middleware import setup_middleware

app = FastAPI(
    title="Task List API",
    description="API para administrar una lista de tareas",
    version="0.1.0",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar middleware de logging
setup_middleware(app)

# Incluir rutas
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/", tags=["health"])
async def health_check():
    """Endpoint para verificar que la API está funcionando."""
    return {"status": "ok", "message": "API is running"}
