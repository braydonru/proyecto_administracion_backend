from fastapi import APIRouter,HTTPException, Depends
from routers.deps.db_session import SessionDep
from models.User import User, User_Create_In
from models.r_user_store import r_user_store
from sqlmodel import select
from typing import List, Annotated
from config.security import hash_password, require_role

users_router = APIRouter(prefix="/user", tags=["User"])

@users_router.get('/get')
def get_users(db:SessionDep, u:Annotated[str,Depends(require_role('SuperAdmin'))]):
    statement = select(User)
    users = db.exec(statement).all()
    return users

@users_router.post('/post')
def create_user(db:SessionDep, u:User_Create_In, us:Annotated[str,Depends(require_role('SuperAdmin'))]):
    user = User(
        username=u.username,
        password=hash_password(u.password),
        name=u.name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@users_router.put('/put')
def set_role(id:int,role:str,db:SessionDep,u:Annotated[str,Depends(require_role('SuperAdmin'))]):
    user = db.get(User,id)
    if not user:
        return HTTPException(status_code=404, detail="User not Found")
    if u['role'] != 'SuperAdmin':
        return HTTPException(status_code=401, detail="User Unauthorized")
    user.role=role
    db.commit()
    db.refresh(user)
    return user

@users_router.post('/create_worker')
def create_worker(w:User_Create_In,store_id:int ,db:SessionDep, u:Annotated[str,Depends(require_role(['Admin','SuperAdmin']))]):
    worker = User(
        username=w.username,
        password=hash_password(w.password),
        name=w.name,
        role='Worker'
    )
    db.add(worker)
    db.flush()

    relation=r_user_store(
        store_id=store_id,
        user_id=worker.id,
        role='Worker'
    )

    db.add(relation)
    db.commit()
    db.refresh(worker)
    return worker

@users_router.delete('/delete')
def delete_user(id:int, db:SessionDep, u:Annotated[str,Depends(require_role(['Admin','SuperAdmin']))]):
    user=db.get(User,id)
    if not user:
        return HTTPException(status_code=404, detail='User not Found')
    db.delete(user)
    db.commit()
    return 'User Deleted'