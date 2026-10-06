from fastapi import FastAPI
from sqlmodel import SQLModel
from config.security import security
from models import *
from config.db import engine
from routers.routers import router
app = FastAPI()

SQLModel.metadata.create_all(engine)



app.include_router(router)
