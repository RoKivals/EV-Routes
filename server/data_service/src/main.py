from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from EV_cars import parse_ev_cars
from database.init_db import init_models
from contextlib import asynccontextmanager
from database import cruds
from database.schemas import CarCreate, CarGet


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting up")
        await init_models()  # Код стартапа
        yield
    finally:
        print("Shutting down...")

app = FastAPI(lifespan=lifespan)


@app.post("/car", response_model=CarCreate)
async def add_car(car: CarCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.add_car(db, car)

@app.post("/cars", response_model=list[CarCreate])
async def add_cars(cars: list[CarCreate], db: AsyncSession = Depends(get_db)):
    return await cruds.add_cars(db, cars)

@app.get("/car", response_model=CarGet)
async def get_car_by_name(name: str, db: AsyncSession = Depends(get_db)):
    return await cruds.get_car_by_name(db, name)

@app.get("/car/{car_id}", response_model=CarGet)
async def get_car(car_id: int, db: AsyncSession = Depends(get_db)):
    return await cruds.get_car(db, car_id)