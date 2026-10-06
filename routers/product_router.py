from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from models.Product import Product, Product_create_in
from models.Store import Store
from models.User import User
from models.r_user_store import r_user_store
from routers.deps.db_session import SessionDep
from typing import Annotated
from config.security import require_role


product_router = APIRouter(prefix='/products', tags=['Products'])

@product_router.get('/get')
def get_products(store_id:int,db:SessionDep, u:Annotated[str,Depends(require_role(['Worker','Admin','SuperAdmin']))]):
    statement = select(Product).where(Product.store_id==store_id)
    products = db.exec(statement)
    return products


@product_router.post('/create_product')
def create_product(product:Product_create_in,store_id:int,db:SessionDep,u:Annotated[str,Depends(require_role(['Worker','Admin','SuperAdmin']))]):
    store = db.get(Store,store_id)
    if not store:
        raise HTTPException(status_code=404, detail='Store not found')
    p = Product(
        name=product.name,
        stock=product.stock,
        store_id=store_id,
        adquisition_price=product.adquisition_price,
        sell_price=product.sell_price
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@product_router.delete('/delete_product')
def delete_product(product_id:int , db:SessionDep,u:Annotated[str,Depends(require_role(['Worker','Admin','SuperAdmin']))]):
    product = db.get(Product,product_id)
    statement = select(r_user_store).where(r_user_store.user_id==u['id'])
    store = db.exec(statement).all()
    if store != product.store_id:
        raise HTTPException(status_code=403, detail='Forbidden')
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    db.delete(product)
    db.commit()
    db.refresh(product)
    return product


@product_router.put('/put')
def modify_price(price:float,product_id:int , db:SessionDep, u:Annotated[str,Depends(require_role(['Admin','SuperAdmin']))]):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    statement = select(Store).where(Store.owner == u['id'], Store.id==product.store_id)
    store = db.exec(statement).first()
    if not store:
        raise HTTPException(status_code=403, detail='Forbidden')
    product.sell_price=price
    db.commit()
    db.refresh(product)
    return product