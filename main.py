from fastapi import FastAPI
from sqlmodel import SQLModel
from config.security import security
from models import *
from config.db import engine
from routers.routers import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(router)
