
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from starlette.exceptions import HTTPException
from models.user import UserModel

from . import schema

class healthCheckDB:
    def check(self, *, db: Session):
        user = db.query(UserModel).first()
        if user:
            return True
        else:
            return False

healthcheck_crud = healthCheckDB()