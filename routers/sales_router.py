from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import select
from models.Sales import Sales, Sales_create_in
from models.Store import Store
from routers.deps.db_session import SessionDep
from config.security import require_role

sales_router = APIRouter(prefix='/sales', tags=['Sales'])

@sales_router.get('/get_sales_by_store')
def get_sales_by_store(store_id:int ,db:SessionDep, u:Annotated[str,Depends(require_role(['Worker','Admin','SuperAdmin']))]):
    statement = select(Sales).where(Sales.store_id==store_id)
    sales = db.exec(statement).all()
    store = db.get(Store, store_id)
    if store.owner != u['id']:
        raise HTTPException(status_code=403, detail='Forbidden')
    if not sales:
        raise HTTPException(status_code=404, detail='Sales not Found')
    return sales