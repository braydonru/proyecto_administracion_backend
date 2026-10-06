from sqlmodel import SQLModel, Field
from typing import Optional
from models.Product import Product
from models.Store import Store
from datetime import date, datetime

class Sales(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True)
    product_id:int = Field(foreign_key='product.id')
    store_id:int = Field(foreign_key='store.id')
    quantity:int=Field(gt=0)
    date:datetime = Field(default_factory=datetime.today)

class Sales_create_in(SQLModel):
    product_id: int = Field(foreign_key='product.id')
    store_id: int = Field(foreign_key='store.id')
    quantity: int = Field(gt=0)