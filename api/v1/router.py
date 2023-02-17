from fastapi import APIRouter
api_router = APIRouter()
from apps.user.endpoints import router as user_endpoints
from apps.healthcheck.endpoints import router as healthcheck_endpoints

api_router.include_router(user_endpoints, prefix='/user', tags=['Пользователи'])
api_router.include_router(healthcheck_endpoints, prefix='/healthcheck', tags=['HealthCheck'])
