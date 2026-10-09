from sqlmodel import SQLModel, Field
from typing import Optional
from models.Product import Product
from models.Store import Store
from datetime import date as date_type, datetime, timezone


class Sales(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True)
    product_id:int = Field(foreign_key='product.id')
    store_id:int = Field(foreign_key='store.id')
    quantity:int=Field(gt=0)
    total_cash:float=Field()
    gained_cash:float=Field()
    date:date_type = Field(default_factory=date_type.today)

class Sales_create_in(SQLModel):
    product_id: int = Field(foreign_key='product.id')
    store_id: int = Field(foreign_key='store.id')
    quantity: int = Field(gt=0)
