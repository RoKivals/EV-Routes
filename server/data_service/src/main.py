from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from EV_cars import parse_ev_cars
from database.database import get_db

from database.init_db import init_models
from contextlib import asynccontextmanager
from database import cruds
from database.schemas import CarCreate, CarGet



@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting up")
        await init_models()

        db_gen = get_db()
        session = await anext(db_gen)
        try:

            if True:
                print("Машины не найдены. Загружаем из API...")
                cars = parse_ev_cars()
                await cruds.add_cars(session, cars)
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

app = FastAPI(lifespan=lifespan, title="EV Route Car Service")
app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST"],
    allow_origins=["*"]
)

@app.post("/car", response_model=CarCreate, status_code=status.HTTP_201_CREATED)
async def add_car(car: CarCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.add_car(db, car)

@app.post("/cars", response_model=list[CarCreate], status_code=status.HTTP_201_CREATED)
async def add_cars(cars: list[CarCreate], db: AsyncSession = Depends(get_db)):
    return await cruds.add_cars(db, cars)

@app.get("/car", response_model=list[CarGet])
async def get_car_by_name(name: str, db: AsyncSession = Depends(get_db)):
    return await cruds.get_car_by_name(db, name)

@app.get("/car/{car_id}", response_model=CarGet)
async def get_car(car_id: int, db: AsyncSession = Depends(get_db)):
    return await cruds.get_car(db, car_id)

@app.get("/cars", response_model=list[CarGet])
async def get_cars(db: AsyncSession = Depends(get_db)):
    return await cruds.get_all_cars(db)