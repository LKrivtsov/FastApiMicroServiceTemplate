from utils.redis import RedisService
from sqlalchemy.orm import Session
from apps.healthcheck.db import healthcheck_crud

redis_service_users = RedisService(db_name="users")

class Logic:
    def check(self, db: Session):
        redis_service_users.set_value("health", "check")
        redis_service_users.delete_key("health")
        healthcheck_crud.check(db=db)
        return {"message": "ok"}

healthcheck_logic = Logic()