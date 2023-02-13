import os
import shutil
import glob

os.system("alembic downgrade -1")

os.remove("./models/models.py")
text_file = open(f"./models/models.py", "w")
n = text_file.write("from sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float\n\nBase = declarative_base()\n")
text_file.close()

os.remove("./api/v1/router.py")
text_file = open(f"./api/v1/router.py", "w")
n = text_file.write("from fastapi import APIRouter\napi_router = APIRouter()\n")
text_file.close()

files = glob.glob('./alembic/versions/*')
for f in files:
    if f != './alembic/versions/__pycache__':
        os.remove(f)

