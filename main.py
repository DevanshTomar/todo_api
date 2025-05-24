from fastapi import FastAPI
import models
from database import engine


app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

def get_db()


