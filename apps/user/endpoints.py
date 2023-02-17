from fastapi import APIRouter, Depends, Body, Request, Form
from typing import Any, List, Union, Optional
from sqlalchemy.orm import Session
from utils.deps import get_db
from apps.user.schema import User, UserInDb, UserSession, AuthorizationResponse
from apps.user.db import user_crud
from fastapi_pagination import Page
from fastapi_filter import FilterDepends
from apps.user.filters import FilterUser
from apps.user.logic import user_logic
from fastapi import Response, Cookie
from models.user import UserModel

router = APIRouter()

@router.post("/register", response_model=UserInDb)
async def register(*, db: Session = Depends(get_db), email: str = Body(...), phone: str = Body(...), password: str = Body(...)):
    return user_logic.registration(db=db, email=email, password=password, phone=phone)

@router.post("/auth", response_model=AuthorizationResponse|Any)
async def auth(response:Response, request:Request,  db: Session = Depends(get_db), login: str = Body(...), password: str = Body(...), auth_type: str = Body(default="token")):
    return user_logic.auth(db=db, response=response, request=request, login=login, password=password, auth_type=auth_type)

@router.get("/me", response_model=UserInDb)
async def get_authorized_user(*, request: Request):
    sessiontoken = user_logic.get_user_session_token(request)
    return user_logic.get_user_by_session_token(session_token=sessiontoken)

@router.get("/get_user_sessions", response_model=List[UserSession])
async def get_user_sessions_list(*, request: Request):
    sessiontoken = user_logic.get_user_session_token(request)
    return user_logic.get_user_sessions(session_token=sessiontoken)

@router.delete("/logout")
async def logout_user(*, sessiontoken: Union[str, None] = Cookie(default=None)):
    return user_logic.close_user_session(session_token=sessiontoken)

@router.delete("/delete_user_session")
async def delete_user_session(*, session_id_to_delete:str, sessiontoken: Union[str, None] = Cookie(default=None)):
    return user_logic.delete_user_session(session_token=session_id_to_delete, sessiontoken=sessiontoken)

@router.get("/", response_model=Page[UserInDb])
async def list(
    *,
    db: Session = Depends(get_db),
    filter: FilterUser = FilterDepends(FilterUser)
):    
    return user_crud.get_multi(filter, db=db)


@router.get("/{id}", response_model=UserInDb)
async def item(*, id: int, db: Session = Depends(get_db)):
    return user_crud.get(db=db, id=id)


@router.post("/", response_model=UserInDb)
async def create(*, item: User, db: Session = Depends(get_db)):
    return user_crud.create(db=db, obj_in=item)


@router.put("/{id}", response_model=UserInDb)
async def item(*, id: int, item: User, db: Session = Depends(get_db)):
    db_obj = user_crud.get(db=db, id=id)
    return user_crud.update(db=db, db_obj=db_obj, obj_in=item)


@router.delete("/{id}", response_model=UserInDb)
async def item(*, id: int, db: Session = Depends(get_db)):
    return user_crud.remove(db=db, id=id)
