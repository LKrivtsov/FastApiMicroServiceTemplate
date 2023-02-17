from typing import Generator

from fastapi import Request


def get_db(request: Request) -> Generator:
    return request.state.db
