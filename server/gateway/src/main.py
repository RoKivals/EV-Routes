from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uvicorn

from server.gateway.src.routers import auth, route
from server.gateway.src.routers import user, station

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


app = FastAPI(title="EV Route Planner Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")
app.include_router(station.router, prefix="/stations")
app.include_router(route.router, prefix="/route")
#app.include_router(data.router, prefix="/data")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Gateway server is starting...")
    yield
    logger.info("Gateway server is shutting down...")


if __name__ == "__main__":
    logger.info("Running with Uvicorn at http://0.0.0.0:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)