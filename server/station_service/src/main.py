from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.database import get_db
from database import cruds
from database.schemas import StationCreate, StationGet
from database.models import Station

from stations import all_stations_info
from database.init_db import init_models
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting up")
        await init_models()

        db_gen = get_db()
        session = await anext(db_gen)
        try:
            result = await session.execute(select(Station).limit(1))
            existing = result.scalar_one_or_none()

            if existing is None:
                print("Станции не найдены. Загружаем из API...")
                origin_stations = all_stations_info()
                await cruds.add_stations(session, origin_stations)
                await session.commit()
            else:
                print("Станции уже есть, пропускаем.")
        except Exception as e:
            await session.rollback()
            print(str(e))
            raise e
        finally:
            await db_gen.aclose()
        yield
    finally:
        print("Shutting down...")

app = FastAPI(lifespan=lifespan, title="EV Route Station Service")
app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST"],
    allow_origins=["*"]
)

@app.post("/station", response_model=StationCreate, status_code=status.HTTP_201_CREATED)
async def add_station(station: StationCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.add_station(db, station)

@app.post("/stations", response_model=list[StationCreate], status_code=status.HTTP_201_CREATED)
async def add_statios(stations: list[StationCreate], db: AsyncSession = Depends(get_db)):
    return await cruds.add_stations(db, stations)

@app.get("/stations", response_model=list[StationGet])
async def get_stations(db: AsyncSession = Depends(get_db)):
    return await cruds.get_all_stations(db)