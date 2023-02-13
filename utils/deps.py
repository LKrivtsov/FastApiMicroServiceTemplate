from fastapi import Request
from typing import Generator


def get_db(request: Request) -> Generator:
    return request.state.db
