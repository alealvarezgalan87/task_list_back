import uuid
import pytest
from fastapi import status

from app.models.task import Task


def test_create_task(client, db, token_headers, test_user):
    """Test para crear una nueva tarea."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
    }
    response = client.post("/api/tasks", json=task_data, headers=token_headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["is_completed"] is False
    assert "id" in data
    assert data["user_id"] == str(test_user.id)
    
    # Verificar que la tarea se guardó en la base de datos
    task = db.query(Task).filter(Task.id == uuid.UUID(data["id"])).first()
    assert task is not None
    assert task.title == task_data["title"]
    assert task.description == task_data["description"]
    assert task.user_id == test_user.id


def test_get_tasks(client, db, token_headers, test_user):
    """Test para obtener todas las tareas del usuario."""
    # Crear algunas tareas para el usuario
    tasks = [
        Task(title="Task 1", description="Description 1", user_id=test_user.id),
        Task(title="Task 2", description="Description 2", user_id=test_user.id),
    ]
    db.add_all(tasks)
    db.commit()
    
    response = client.get("/api/tasks", headers=token_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_task(client, db, token_headers, test_user):
    """Test para obtener una tarea específica."""
    # Crear una tarea para el usuario
    task = Task(title="Test Task", description="Description", user_id=test_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    
    response = client.get(f"/api/tasks/{task.id}", headers=token_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == task.title
    assert data["description"] == task.description
    assert data["id"] == str(task.id)


def test_get_task_not_found(client, token_headers):
    """Test para verificar que no se puede obtener una tarea que no existe."""
    non_existent_id = uuid.uuid4()
    response = client.get(f"/api/tasks/{non_existent_id}", headers=token_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Tarea no encontrada" in response.json()["detail"]


def test_get_task_unauthorized(client, db, token_headers, test_user):
    """Test para verificar que no se puede obtener una tarea de otro usuario."""
    # Crear un usuario diferente
    other_user_id = uuid.uuid4()
    
    # Crear una tarea para el otro usuario
    task = Task(title="Other User Task", description="Description", user_id=other_user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    
    response = client.get(f"/api/tasks/{task.id}", headers=token_headers)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "No tienes permiso" in response.json()["detail"]


def test_update_task(client, db, token_headers, test_user):
    """Test para actualizar una tarea."""
    # Crear una tarea para el usuario
    task = Task(title="Original Title", description="Original Description", user_id=test_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "is_completed": True,
    }
    response = client.put(f"/api/tasks/{task.id}", json=update_data, headers=token_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["is_completed"] == update_data["is_completed"]
    
    # Verificar que la tarea se actualizó en la base de datos
    updated_task = db.query(Task).filter(Task.id == task.id).first()
    assert updated_task.title == update_data["title"]
    assert updated_task.description == update_data["description"]
    assert updated_task.is_completed == update_data["is_completed"]


def test_delete_task(client, db, token_headers, test_user):
    """Test para eliminar una tarea."""
    # Crear una tarea para el usuario
    task = Task(title="Task to Delete", description="Description", user_id=test_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    
    response = client.delete(f"/api/tasks/{task.id}", headers=token_headers)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verificar que la tarea se eliminó de la base de datos
    deleted_task = db.query(Task).filter(Task.id == task.id).first()
    assert deleted_task is None
