from pydantic import BaseModel

class Healthcheck(BaseModel):
    message: str