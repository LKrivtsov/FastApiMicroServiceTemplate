import yaml
from pprint import pprint
import os

def get_col_type(col_name, app):
    for col in app['table_cols']:
        if col['name'] == col_name:
            return col['type']    

def get_col_full_type(name):
    if name == 'int':
        return "Integer"
    if name == 'str':
        return "String"
    if name == 'bool':
        return "Boolean"
    if name == 'datetime':
        return "DateTime"
    if name == 'roreign_key':
        return 'ForeignKey'
    if name == 'float':
        return 'Float'

with open("config.yml", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    for app in data["apps"]:
        # create dir
        os.makedirs(f"./apps/{app['name'].lower()}")
        # create db file
        text_file = open(f"./apps/{app['name'].lower()}/db.py", "w")
        n = text_file.write(
            """from db.base_crud import CRUDBase
from models.models import {name}Model
from . import schema


class {name}DB(CRUDBase[{name}Model, schema.{name}, schema.{name}InDb]):
    pass


{name_lower}_crud = {name}DB({name}Model)
        """.format(
                name=app["name"], name_lower=app["name"].lower()
            )
        )
        text_file.close()
        # create endpoints file
        text_file = open(f"./apps/{app['name'].lower()}/endpoints.py", "w")
        n = text_file.write(
            """from fastapi import APIRouter, Depends
from typing import Any, List
from sqlalchemy.orm import Session
from utils.deps import get_db
from apps.{name_lower}.schema import {name}, {name}InDb
from apps.{name_lower}.db import {name_lower}_crud
from fastapi_pagination import Page
from fastapi_filter import FilterDepends
from apps.{name_lower}.filters import Filter{name}

router = APIRouter()


@router.get("/", response_model=Page[{name}InDb])
async def list(
    *,
    db: Session = Depends(get_db),
    filter: Filter{name} = FilterDepends(Filter{name})
):    
    return {name_lower}_crud.get_multi(filter, db=db)


@router.get("/{id}", response_model={name}InDb)
async def item(*, id: int, db: Session = Depends(get_db)):
    return {name_lower}_crud.get(db=db, id=id)


@router.post("/", response_model={name}InDb)
async def create(*, item: {name}, db: Session = Depends(get_db)):
    return {name_lower}_crud.create(db=db, obj_in=item)


@router.put("/{id}", response_model={name}InDb)
async def item(*, id: int, item: {name}, db: Session = Depends(get_db)):
    db_obj = {name_lower}_crud.get(db=db, id=id)
    return {name_lower}_crud.update(db=db, db_obj=db_obj, obj_in=item)


@router.delete("/{id}", response_model={name}InDb)
async def item(*, id: int, db: Session = Depends(get_db)):
    return {name_lower}_crud.remove(db=db, id=id)
""".format(
                name=app["name"], name_lower=app["name"].lower(), id="{id}"
            )
        )
        text_file.close()
        # create schema file
        main_schema = ""
        for schema_item in app["table_cols"]:
            if schema_item["name"] != "id":
                schema = f"  {schema_item['name']}: {schema_item['type']}\n"
                main_schema += schema
        text_file = open(f"./apps/{app['name'].lower()}/schema.py", "w")
        n = text_file.write(
            """from typing import List
from pydantic import BaseModel

class {name}(BaseModel):    
{main_schema}

class {name}InDb({name}):
    id: int    

    class Config:
        orm_mode = True
""".format(
                main_schema=main_schema, name=app["name"]
            )
        )
        text_file.close()
        # create filters file
        main_filter = ""
        for filter_item in app["filters"]:      
            for filter_type in filter_item["types"]:
                if filter_type == "eq":
                    filter = f"    {filter_item['col']}: Optional[{get_col_type(filter_item['col'], app)}]\n"
                else:
                    filter = f"    {filter_item['col']}__{filter_type}: Optional[{get_col_type(filter_item['col'], app)}]\n"
                main_filter += filter
        text_file = open(f"./apps/{app['name'].lower()}/filters.py", "w")
        n = text_file.write(
            """from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from models.models import {name}Model


class Filter{name}(Filter):
{main_filter}
    class Constants(Filter.Constants):
        model = {name}Model

    order_by: Optional[list[str]]""".format(
                main_filter=main_filter, name=app["name"]
            )
        )
        text_file.close()

        # add to models
        columns = ""
        for col in app["table_cols"]:
            if col["name"] == "id":
                column = "    id = Column(Integer, primary_key=True, index=True)\n"
            else:
                column = f"    {col['name']} = Column({get_col_full_type(col['type'])})\n"
            columns += column
        
        text_file = open(f"./models/models.py", "a")
        n = text_file.write(
            """class {name}Model(Base):
    __tablename__ = "{table_name}"
{columns}""".format(
                name=app["name"], table_name=app["table_name"], columns=columns
            )
        )
        text_file.close()
        
        # add to routes
        text_file = open(f"./api/v1/router.py", "a")
        text_file.write(f"from apps.{app['name'].lower()}.endpoints import router as {app['name'].lower()}_endpoints\n")
        text_file.write(f"api_router.include_router({app['name'].lower()}_endpoints, prefix='/{app['name'].lower()}', tags=['{app['humanized_name']}'])\n")
        
        text_file.close()

os.system("python -m alembic revision --autogenerate -m 'first migration' && python -m alembic upgrade head")