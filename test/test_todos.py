from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from sqlalchemy.pool import StaticPool
from main import app
from routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
import pytest
from models import Todos

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

Testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = Testing_session_local()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"user_name": "test", "user_id": 1, "role": "user"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture()
def test_todo():
    todo = Todos(title="test", description="test", priority=1, complete=False, owner_id=1)
    
    db = Testing_session_local()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": test_todo.id, "title": test_todo.title, "description": test_todo.description, "priority": test_todo.priority, "complete": test_todo.complete, "owner_id": test_todo.owner_id}]

def test_read_one_authenticated(test_todo):
    response = client.get(f"/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": test_todo.id, "title": test_todo.title, "description": test_todo.description, "priority": test_todo.priority, "complete": test_todo.complete, "owner_id": test_todo.owner_id}

def test_read_one_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

def test_read_one_unauthenticated(test_todo):
    def override_get_current_user_unauthorized():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    original_override = app.dependency_overrides[get_current_user]
    app.dependency_overrides[get_current_user] = override_get_current_user_unauthorized
    
    try:
        response = client.get(f"/todo/{test_todo.id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "User not found"}
    finally:
        app.dependency_overrides[get_current_user] = original_override
    




    