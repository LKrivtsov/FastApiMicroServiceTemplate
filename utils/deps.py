from fastapi import Request, Depends
from typing import Generator
import string
import random
from starlette.exceptions import HTTPException
# import redis
# from utils.redis import RedisService

# redis_service_sessions = RedisService(db_name="sessions")

def get_db(request: Request) -> Generator:
    return request.state.db

def generate_random_string(stringLength=12):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

# def get_current_user():
#     print("user")
#     data = redis_service_sessions.get_value(session_token)
#     if data:
#         return data
#     else:
#         raise HTTPException(status_code=401, detail="user session expired")
#     # print(session_token)
    
#     # print(token)
#     pass