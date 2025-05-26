from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from database.models import Base
from EV_cars import parse_ev_cars
from database.init_db import init_models
from contextlib import asynccontextmanager
from database import cruds
from database.schemas import CarCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting up")
        await init_models()  # Код стартапа
        yield
    finally:
        print("Shutting down...")

app = FastAPI(lifespan=lifespan)


@app.post("/cars", response_model=CarCreate)
async def add_car(car: CarCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.add_car(db, car)