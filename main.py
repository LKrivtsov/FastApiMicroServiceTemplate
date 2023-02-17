from settings import settings
from fastapi import FastAPI, Request, Response
from db.session import SessionLocal
from api.v1.router import api_router
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware



app = FastAPI(title=settings.PROJECT_NAME)

add_pagination(app)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://10.3.0.72:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY, same_site="none", https_only=True)

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
        pass
        request.state.db.commit()
        request.state.db.close()
    return response
