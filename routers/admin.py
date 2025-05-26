from fastapi import APIRouter, HTTPException, Depends, Path, status
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Todos, Users
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)
  
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/todos', status_code=status.HTTP_200_OK)
def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    if user.get("role").casefold() != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized")
    
    return db.query(Todos).all()



@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    if user.get("role").casefold() != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized")
    
    todo_model: Todos | None = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).delete(synchronize_session=False)
    
    db.commit()

    

