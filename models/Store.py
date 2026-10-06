from sqlmodel import SQLModel, Field
from typing import Optional

class Store(SQLModel, table=True):
    id:Optional[int]=Field(primary_key=True)
    name:str = Field()
    owner:Optional[int] = Field(foreign_key='user.id')

class Store_create_in(SQLModel):
    name:str = Field()
    owner:int = Field()
