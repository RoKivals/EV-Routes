from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from database.database import get_db
from database import cruds
from database.schemas import StationCreate, StationGet
from database.models import Station

from stations import all_stations_info
from database.init_db import init_models
from contextlib import asynccontextmanager

async def initialize_stations():
    """Инициализация станций в базе данных при первом запуске"""
    async for session in get_db():
        try:
            result = await session.execute(select(func.count(Station.id)))
            count = result.scalar()
            
            if count == 0:
                print("База данных пуста. Загружаем станции из API...")
                origin_stations = all_stations_info()
                
                if origin_stations:
                    await cruds.add_stations(session, origin_stations)
                    await session.commit()
                    print(f"Успешно загружено {len(origin_stations)} станций")
                else:
                    print("Не удалось получить данные о станциях из API")
            else:
                print(f"В базе данных уже есть {count} станций. Пропускаем инициализацию.")
                
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при инициализации станций: {str(e)}")
            raise
        finally:
            break

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Запуск приложения...")
        
        # Инициализация моделей БД
        await init_models()
        print("Модели базы данных инициализированы")
        
        # Инициализация данных
        await initialize_stations()
        
        print("Приложение успешно запущено")
        yield
        
    except Exception as e:
        print(f"Ошибка при запуске приложения: {str(e)}")
        raise
    finally:
        print("Завершение работы приложения...")

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