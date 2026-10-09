from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import select
from models.Sales import Sales, Sales_create_in
from models.Store import Store
from models.Product import Product
from routers.deps.db_session import SessionDep
from config.security import require_role
from sqlalchemy import func

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


@sales_router.post('/create_sales')
def create_sales(sale:Sales_create_in,u:Annotated[str,Depends(require_role(['Admin','SuperAdmin']))],db:SessionDep):
    store = db.get(Store, sale.store_id)
    product = db.get(Product, sale.product_id)

    if not store or not product:
        raise HTTPException(status_code=404, detail='Not found')
    if store.owner != u['id'] or product.store_id != store.id:
        raise HTTPException(status_code=403, detail='Forbidden')
    if product.stock<sale.quantity:
        raise HTTPException(status_code=403, detail='There is not enough')

    s = Sales(
        store_id=sale.store_id,
        product_id=sale.product_id,
        quantity=sale.quantity,
        total_cash=product.sell_price*sale.quantity,
        gained_cash=(product.sell_price-product.adquisition_price) * sale.quantity
    )
    product.stock -= sale.quantity
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@sales_router.get('/get_inventory')
def get_inventory(store_id:int, db:SessionDep, u:Annotated[str,Depends(require_role(['Admin', 'SuperAdmin']))]):
    store = db.get(Store, store_id)
    if u['id'] != store.owner:
        raise HTTPException(status_code=403, detail='Forbidden')


    statement = (
        select(
            Product.id,
            Product.name,
            Product.stock,
            Sales.date,
            func.sum(Sales.total_cash).label("total_cash"),
            func.sum(Sales.gained_cash).label("gained_cash"),
        )
        .join(Product, Product.id == Sales.product_id)
        .where(Sales.store_id == store_id)
        .group_by(Product.id, Product.name, Sales.date, Product.stock)
    )
    sales = db.exec(statement).mappings().all()
    return sales