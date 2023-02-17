from db.base_crud import CRUDBase
from models.user import UserModel
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from db.base_class import Base
from starlette.exceptions import HTTPException

from . import schema

class UserDB(CRUDBase[UserModel, schema.User, schema.UserInDb]):

    def user_exist(self, *, db: Session, email:str, phone:str) -> schema.UserInDb:
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if user:
            return user
        else:
            user = db.query(UserModel).filter(UserModel.phone == phone).first()
            if user:
                return user
            else:
                False
                
    def find_user_by_login(self, *, db: Session, login:str) -> schema.UserInDb:
        user = db.query(UserModel).filter(UserModel.email == login).first()
        if user:
            return user
        else:
            user = db.query(UserModel).filter(UserModel.phone == login).first()
            if user:
                return user
            else:
                False

    def create_user(self, *, db: Session, obj_in: dict) -> schema.UserInDb:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user_crud = UserDB(UserModel)
        