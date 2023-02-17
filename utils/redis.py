import pickle
from typing import Any, Optional
from datetime import timedelta

import redis

from settings import settings

class RedisService:
    def __init__(self, db_name):
        match db_name:
            case "sessions":
                self.redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PWD, db=settings.REDIS_DB_SESSIONS)
            case "users":
                self.redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PWD, db=settings.REDIS_DB_USERS)


    def get_value(self, key: str) -> Optional[Any]:
        """
        Get value by key from the redis if exists, else return None
        """
        value = None
        try:
            value = self.redis_cli.get(key)
            if value:
                value = pickle.loads(value)                
        except Exception as e:
            print(f"Exception in getting value with key ({key}) from the redis: ", str(e))

        return value

    def set_value(self, key: str, value: Any, expire_minutes: int = -1) -> None:
        """
        Set a value to a key in Redis
        """
        try:
            value = pickle.dumps(value)
            if expire_minutes == -1:
                self.redis_cli.set(key, value)
            else:
                self.redis_cli.setex(key, timedelta(minutes=expire_minutes), value)                
        except Exception as e:
            print(f"Exception in setting value with key ({key}) to the redis: ", str(e))

    def is_exists(self, key: str) -> bool:
        """ Return True if given key exists in the Redis, otherwise return False. """
        try:
            return bool(self.redis_cli.exists(key))
        except Exception as e:
            print(f"Exception in checking key existing ({key}) in the redis: ", str(e))
            return False

    def delete_key(self, key: str) -> None:
        """
        Delete a key if exists from Redis
        """
        try:
            if self.get_value(key):
                self.redis_cli.delete(key)
        except Exception as e:
            print(f"Exception in deleting key ({key}) from the redis: ", str(e))


# redis_service = RedisService()
