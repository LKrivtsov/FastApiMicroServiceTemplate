from pydantic import BaseSettings, validator
from typing import Any, Dict, List, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str
    # DB
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_NAME: str

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        DB_USER = values.get("DB_USER")
        DB_PASSWORD = values.get("DB_PASSWORD")
        DB_HOST = values.get("DB_HOST")
        DB_PORT = values.get("DB_PORT")
        DB_NAME = values.get("DB_NAME")
        CON_STR = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        return CON_STR

    POOL_SIZE: int
    MAX_OVERFLOW: int
    POOL_RECYCLE: int

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
