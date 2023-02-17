from fastapi import APIRouter, Depends
from apps.healthcheck.schema import Healthcheck
from sqlalchemy.orm import Session
from utils.deps import get_db
from apps.healthcheck.logic import healthcheck_logic
router = APIRouter()


@router.get("/", response_model=Healthcheck)
def heathcheck(db: Session = Depends(get_db)):
    return healthcheck_logic.check(db=db)
