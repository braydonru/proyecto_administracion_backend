from sqlmodel import SQLModel, Field
from typing import Optional
from models.Store import Store
from models.User import User


class r_user_store(SQLModel, table=True):
    id:Optional[int]=Field(primary_key=True)
    store_id:Optional[int]=Field(foreign_key='store.id')
    user_id:Optional[int]=Field(foreign_key='user.id')
    role:str=Field()