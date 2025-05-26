from fastapi import APIRouter, HTTPException, Depends, Path, status
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Todos, Users
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from passlib.context import CryptContext
from .auth import create_access_token

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
  
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "password": "testpassword",
                "new_password": "testpassword2"
            }
        }
    }

@router.get('/', status_code=status.HTTP_200_OK)
def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return db.query(Users).filter(Users.id == user.get("user_id")).first()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
def change_password(db: db_dependency, user: user_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    user_model: Users | None = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()



