from fastapi import APIRouter, HTTPException, Depends, Path, status
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Todos
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(
    tags=["todos"],
)
  
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool 

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Example title",
                "description": "Example description",
                "priority": 1,
                "complete": False
            }
        }
    }

@router.get('/', status_code=status.HTTP_200_OK)
def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return db.query(Todos).filter(Todos.owner_id == user["user_id"]).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    todo_model: Todos | None = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("user_id")).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    return todo_model

@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo: TodoRequest):
    todo_model = Todos(**todo.model_dump(), owner_id=user.get("user_id"))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, user: user_dependency, todo: TodoRequest, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    todo_model: Todos | None = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("user_id")).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    db.add(todo_model)
    db.commit()

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    todo_model: Todos | None = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("user_id")).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("user_id")).delete(synchronize_session=False)

    db.commit()
