from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):  # noqa: WPS115
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
        db_user = values.get("DB_USER")
        db_password = values.get("DB_PASSWORD")
        db_host = values.get("DB_HOST")
        db_port = values.get("DB_PORT")
        db_name = values.get("DB_NAME")
        connection_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return connection_str

    POOL_SIZE: int
    MAX_OVERFLOW: int
    POOL_RECYCLE: int

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
