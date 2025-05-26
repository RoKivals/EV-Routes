from fastapi import FastAPI, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from stations import get_all_stations
from database.init_db import init_models
from contextlib import asynccontextmanager
from database import cruds
from database.schemas import StationCreate, StationGet


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting up")
        app.add_middleware(
            allow_methods=["GET", "POST"],
            allow_origins=["*"]
        )
        await init_models()
        yield
    finally:
        print("Shutting down...")

app = FastAPI(lifespan=lifespan, title="EV Route Station Service")


@app.post("/station", response_model=StationCreate, status_code=status.HTTP_201_CREATED)
async def add_station(station: StationCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.add_station(db, station)

@app.post("/stations", response_model=list[StationCreate], status_code=status.HTTP_201_CREATED)
async def add_statios(stations: list[StationCreate], db: AsyncSession = Depends(get_db)):
    return await cruds.add_stations(db, stations)

@app.get("/stations", response_model=StationGet)
async def get_stations(db: AsyncSession = Depends(get_db)):
    return await cruds.get_all_stations(db)