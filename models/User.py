from sqlalchemy import table, true, ForeignKey
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True)
    username:str = Field(unique=True)
    password:str = Field()
    name:str = Field()
    role:str = Field()

class User_Create_In(SQLModel):
    username: str = Field()
    password: str = Field()
    name: str = Field()