from fastapi import FastAPI
from routers.data import router as data_router
from routers.user import router as user_router
from routers.station import router as station_router
from routers.route import router as route_router

def include_routes(app: FastAPI):
    app.include_router(data_router, prefix="/data")
    app.include_router(user_router, prefix="/user")
    app.include_router(station_router, prefix="/station")
    app.include_router(route_router, prefix="/route")