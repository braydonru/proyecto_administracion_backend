from fastapi import APIRouter, Depends, HTTPException
from models.Store import Store, Store_create_in
from routers.deps.db_session import SessionDep
from sqlmodel import select
from typing import Annotated
from config.security import require_role
store_router = APIRouter(prefix='/store', tags=['Store'])

@store_router.get('/get')
def get_stores(db:SessionDep, u:Annotated[str,Depends(require_role('SuperAdmin'))]):
    statement = select(Store)
    stores = db.exec(statement).all()
    return stores

@store_router.get('/get_by_owner')
def get_store_by_owner(db:SessionDep,  u:Annotated[str,Depends(require_role('Admin'))]):
    statement= select(Store).filter(Store.owner==u['id'])
    store = db.exec(statement).all()
    return store

@store_router.post('/create')
def create_store(db:SessionDep, store:Store_create_in, u:Annotated[str,Depends(require_role('SuperAdmin'))]):
    s=Store(
        name=store.name,
        owner=store.owner,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@store_router.delete('/delete')
def delete_store(store_id:int, db:SessionDep,  u:Annotated[str,Depends(require_role('SuperAdmin'))]):
    store = db.get(Store,store_id)
    if not store:
        return HTTPException(status_code=404, detail='Store not found')
    db.delete(store)
    db.commit()
    return "Store deleted"