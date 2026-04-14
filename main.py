from fastapi import FastAPI
from routers import notes, users
from database import engine, Base
from models import User, Note

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(notes.router)
app.include_router(users.router)
