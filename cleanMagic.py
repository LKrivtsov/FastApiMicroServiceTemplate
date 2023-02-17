import glob
import os
import shutil

import yaml

with open("config.yml", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    for app in data["apps"]:
        shutil.rmtree(f"./apps/{app['name'].lower()}")

os.system("alembic downgrade -1")

# os.remove("./models/models.py")
# text_file = open(f"./models/models.py", "w")
# n = text_file.write("from sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float\nfrom db.base_class import Base\n")
# text_file.close()

files = glob.glob("./models/*")
for f in files:
    if f != "./models/__init__.py" and f != "./models/__pycache__":
        os.remove(f)

os.remove("./api/v1/router.py")
text_file = open(f"./api/v1/router.py", "w")
n = text_file.write("from fastapi import APIRouter\napi_router = APIRouter()\n")
text_file.close()

files = glob.glob("./alembic/versions/*")
for f in files:
    if f != "./alembic/versions/__pycache__":
        os.remove(f)
