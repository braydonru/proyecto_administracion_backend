from sqlmodel import SQLModel, Field
from typing import Optional

class mksita (SQLModel, table=True):
    id:Optional[int]=Field(primary_key=True)
    name:str=Field()
    es_lesbiana:bool=Field()
    dinero_en_efectivo:float= Field()


class mksita_create_in(SQLModel):
    name:str=Field()
    es_lesbiana: bool = Field()
    dinero_en_efectivo: float = Field()