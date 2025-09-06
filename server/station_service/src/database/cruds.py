from database.schemas import StationCreate, StationGet
from database.models import Station

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def add_station(db: AsyncSession, station: StationCreate) -> Station:
    new_station = Station(name=station.name,
                    latitude=station.latitude,
                    longitude=station.longtitude, 
                    connection_type=station.connection_type,
                    power_kw=station.power_kw)
    db.add(new_station)
    await db.flush()
    return new_station

async def add_stations(db: AsyncSession, stations: list[StationCreate]) -> list[Station]:
    station_objects = [
                Station(name=station.name,
                    latitude=station.latitude,
                    longitude=station.longtitude, 
                    connection_type=station.connection_type,
                    power_kw=station.power_kw)
            for station in stations
    ]

    db.add_all(station_objects)
    await db.flush()
    return station_objects

async def get_all_stations(db: AsyncSession) -> list[StationGet]:
    stmt = select(Station)

    result = await db.execute(statement=stmt)
    return result.scalars().all()
