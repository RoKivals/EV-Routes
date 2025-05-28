from fastapi import FastAPI
from .auth import router as auth_router
from .user import router as user_router
from .station import router as station_router

def include_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(station_router)