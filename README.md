# Task List API

API REST desarrollada con FastAPI y PostgreSQL para administrar una lista de tareas (TODOs).

## Características

- Autenticación de usuarios con JWT
- CRUD completo para tareas
- Persistencia en PostgreSQL
- Migraciones con Alembic
- Dockerización con Docker Compose
- Tests automatizados
- Logging para errores y auditoría

## Requisitos

- Python 3.9+
- PostgreSQL
- Docker y Docker Compose (opcional)

## Estructura del Proyecto

```
task_list_back/
├── alembic/                # Migraciones de base de datos
│   └── versions/           # Scripts de migración
├── app/
│   ├── api/                # Endpoints de la API
│   │   └── routes/         # Rutas de la API
│   ├── core/               # Configuración central
│   ├── db/                 # Configuración de la base de datos
│   ├── models/             # Modelos SQLAlchemy
│   ├── schemas/            # Esquemas Pydantic
│   └── tests/              # Tests automatizados
├── .env                    # Variables de entorno
├── alembic.ini             # Configuración de Alembic
├── docker-compose.yml      # Configuración de Docker Compose
├── Dockerfile              # Configuración de Docker
└── requirements.txt        # Dependencias del proyecto
```

## Instalación y Ejecución

### Opción 1: Con Docker Compose (recomendado)

1. Clona el repositorio:
   ```bash
   git clone https://github.com/alealvarezgalan87/task_list_back.git
   cd task_list_back
   ```

2. Inicia los servicios con Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Ejecuta las migraciones:
   ```bash
   docker-compose exec api alembic upgrade head
   ```

4. La API estará disponible en: http://localhost:8000

### Opción 2: Instalación Local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/alealvarezgalan87/task_list_back.git
   cd task_list_back
   ```

2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En Linux/Mac
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura la base de datos PostgreSQL y actualiza los archivos `.env` y `alembic.ini` con tus credenciales.

5. Ejecuta las migraciones:
   ```bash
   alembic upgrade head
   ```

6. Inicia el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

7. La API estará disponible en: http://localhost:8000

## Uso de la API

### Documentación

La documentación interactiva de la API está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Ejemplos de Uso

#### Registro de Usuario

```bash
curl -X 'POST' \
  'http://localhost:8000/api/auth/register' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "usuario@example.com",
  "username": "usuario",
  "password": "contraseña123"
}'
```

#### Inicio de Sesión

```bash
curl -X 'POST' \
  'http://localhost:8000/api/auth/login' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=usuario@example.com&password=contraseña123'
```

#### Crear una Tarea

```bash
curl -X 'POST' \
  'http://localhost:8000/api/tasks' \
  -H 'Authorization: Bearer <tu-token>' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Mi primera tarea",
  "description": "Descripción de la tarea"
}'
```

#### Obtener Todas las Tareas

```bash
curl -X 'GET' \
  'http://localhost:8000/api/tasks' \
  -H 'Authorization: Bearer <tu-token>'
```

#### Obtener una Tarea Específica

```bash
curl -X 'GET' \
  'http://localhost:8000/api/tasks/{id}' \
  -H 'Authorization: Bearer <tu-token>'
```

#### Actualizar una Tarea

```bash
curl -X 'PUT' \
  'http://localhost:8000/api/tasks/{id}' \
  -H 'Authorization: Bearer <tu-token>' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Tarea actualizada",
  "description": "Nueva descripción",
  "is_completed": true
}'
```

#### Eliminar una Tarea

```bash
curl -X 'DELETE' \
  'http://localhost:8000/api/tasks/{id}' \
  -H 'Authorization: Bearer <tu-token>'
```

## Ejecución de Tests

Para ejecutar los tests automatizados:

```bash
pytest app/tests
```

## Consideraciones Técnicas

### Alta Concurrencia
- Se utilizan sesiones de base de datos independientes para cada solicitud
- SQLAlchemy gestiona eficientemente el pool de conexiones

### Grandes Volúmenes de Datos
- Implementación de paginación en los endpoints de listado
- Índices en la base de datos para optimizar consultas

### Escenarios de Error
- Validación de datos con Pydantic
- Manejo centralizado de excepciones
- Logging detallado para facilitar la depuración

### Seguridad
- Autenticación con JWT
- Contraseñas hasheadas con bcrypt
- Verificación de permisos para acceder a recursos
