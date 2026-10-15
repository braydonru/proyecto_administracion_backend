from models.test_mksita import mksita, mksita_create_in
from fastapi import APIRouter
from routers.deps.db_session import SessionDep
from sqlmodel import select

test_router = APIRouter(prefix='/test',tags=['test'])



@test_router.get('/get')
def test_get(db:SessionDep):
    statement = select(mksita)
    tests = db.exec(statement).all()
    return tests

@test_router.post('/post')
def test_post(db:SessionDep, t:mksita_create_in):
    mk = mksita(
        name=t.name,
        es_lesbiana=t.es_lesbiana,
        dinero_en_efectivo=t.dinero_en_efectivo
    )
    db.add(mk)
    db.commit()
    db.refresh(mk)
    return mk

@test_router.delete('/delete')
def test_delete(id:int,db:SessionDep):
    t = db.get(mksita, id)
    db.delete(t)
    db.commit()
    return 'Deleted'