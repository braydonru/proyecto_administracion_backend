from sqlmodel import SQLModel, Field
from typing import Optional
from models.Store import Store


class Product(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True)
    name:str = Field()
    stock: int = Field(gt=0, default=0)
    adquisition_price: float = Field(ge=0)
    sell_price: float = Field(ge=0)
    store_id:Optional[int] = Field(foreign_key='store.id')


class Product_create_in(SQLModel):
    name: str = Field()
    stock: int = Field(gt=0, default=0)
    adquisition_price: float = Field(ge=0)
    sell_price: float = Field(ge=0)