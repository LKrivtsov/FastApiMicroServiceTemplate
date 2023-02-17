from fastapi import FastAPI, Request, Response
from fastapi_pagination import add_pagination

from api.v1.router import api_router
from db.session import SessionLocal
from settings import settings

app = FastAPI(title=settings.PROJECT_NAME)

add_pagination(app)

app.include_router(api_router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except Exception as ex:
        import traceback

        traceback.print_exc()
        print("exc: ", str(ex))
        request.state.db.rollback()
    finally:
        request.state.db.commit()
        request.state.db.close()
    return response
