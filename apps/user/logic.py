from sqlalchemy.orm import Session
from apps.user.db import user_crud
from datetime import datetime
from passlib.hash import django_pbkdf2_sha256
from starlette.exceptions import HTTPException
from utils.deps import generate_random_string
from fastapi import Response, Request
import uuid
from utils.redis import RedisService

redis_service_sessions = RedisService(db_name="sessions")
redis_service_users = RedisService(db_name="users")

class Logic:
    def registration(self, db: Session, *, email: str, password: str, phone: str):
        if not user_crud.user_exist(db=db, email=email, phone=phone):
            hashed_password = django_pbkdf2_sha256.using(salt=generate_random_string(12), rounds=12000).hash(password)
            user_obj = {
                "email": email,
                "password": hashed_password,
                "middlename": None,
                "firstname": None,
                "lastname": None,
                "is_email_confirmed": False,
                "email_confirmed_at": None,
                "phone": phone,
                "iin": None,
                "is_active": False,
                "is_admin": False,
                "created_at": datetime.now(),
                "last_seen_at": datetime.now(),
                "id_card": None,
                "is_phone_confirmed": False,
                "phone_confirmed_at": None,
            }
            user = user_crud.create_user(db=db, obj_in=user_obj)
        else:
            raise HTTPException(status_code=409, detail="user already exists")
        return user

    def get_user_by_session_token(self, session_token: str):
        data = redis_service_sessions.get_value(session_token)
        if data:
            return data
        else:
            raise HTTPException(status_code=401, detail="user session expired")

    def get_user_session_token(self, request: Request):        
        if "authorization" not in request.headers:     
            if "sessiontoken" in request.cookies:
                return request.cookies["sessiontoken"]        
        else:            
            return request.headers["authorization"].split(" ")[1]

    def get_user_sessions(self, session_token: str):
        user = redis_service_sessions.get_value(session_token)
        if user and redis_service_users.is_exists(user.id):
            sessions_info = redis_service_users.get_value(user.id)
        else:
            raise HTTPException(status_code=401, detail="user has no sessions")
        if sessions_info:
            sessions_array = []
            for session_id in sessions_info:
                sessions_array.append({"session_id": session_id})            
            return sessions_array
        else:
            raise HTTPException(status_code=401, detail="user has no sessions")

    def close_user_session(self, session_token: str):
        if redis_service_sessions.is_exists(session_token):
            user = redis_service_sessions.get_value(session_token)
            sessions_info = redis_service_users.get_value(user.id)
            sessions_info.remove(session_token)
            sessions_info = redis_service_users.set_value(user.id, sessions_info)
            redis_service_sessions.delete_key(session_token)            
            return {"status_code": 200, "detail": "session has been closed"}
        else:
            raise HTTPException(status_code=401, detail="session doesn't exist")

    def delete_user_session(self, session_token: str, sessiontoken: str):
        user_sessions_array = self.get_user_sessions(sessiontoken)
        user = redis_service_sessions.get_value(sessiontoken)
        sessions_info = redis_service_users.get_value(user.id)
        for item in sessions_info:
            if item == sessiontoken:
                if session_token in sessions_info:
                    sessions_info.remove(session_token)
                    sessions_info = redis_service_users.set_value(user.id, sessions_info)
                    redis_service_sessions.delete_key(session_token)
                    return {"status_code": 200, "detail": "session has been closed"}
                else:
                    raise HTTPException(status_code=401, detail="session doesn't exist")            
        raise HTTPException(status_code=401, detail="session doesn't exist")

    def auth(self, db: Session, *, response: Response, request:Request, login: str, password: str, auth_type:str):
        print(login)
        print(password)
        user = user_crud.find_user_by_login(db=db, login=login)
        if user is None:
            raise HTTPException(status_code=401, detail="user not found")
        else:
            if django_pbkdf2_sha256.verify(password, user.password):
                session_token = str(uuid.uuid4())
                redis_service_sessions.set_value(session_token, user, 1440)
                userdata = redis_service_users.get_value(user.id)
                if userdata is None:
                    redis_service_users.set_value(user.id, [session_token], 1440)
                else:
                    userdata.append(session_token)
                    redis_service_users.set_value(user.id, userdata, 1440)
                if auth_type == "cookie":
                    # response.set_cookie(key="sessiontoken", value=session_token, samesite='none', secure=True, httponly=True, domain="http://localhost:3000")
                    request.session["sessiontoken"] = session_token
                    return {"status_code": 200, "detail": "login successful"}
                else:
                    return {"access_token": session_token, "token_type": "Bearer"}
            else:
                raise HTTPException(status_code=401, detail="incorrect password")


user_logic = Logic()