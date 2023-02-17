from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from models.user import UserModel


class FilterUser(Filter):
    email: Optional[str]

    class Constants(Filter.Constants):
        model = UserModel

    order_by: Optional[list[str]]