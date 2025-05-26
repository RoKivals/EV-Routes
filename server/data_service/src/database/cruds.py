from database.schemas import CarCreate, CarGet
from database.models import Car

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def add_car(db: AsyncSession, car: CarCreate) -> Car:
    new_car = Car(name=car.name, 
                  battery_capacity=car.battery_capacity,
                  consumpting=car.consumpting,
                  type_charger=car.type_charger)
    db.add(new_car)
    await db.flush()
    return new_car

async def add_cars(db: AsyncSession, cars: list[CarCreate]) -> list[Car]:
    car_objects = [
        Car(name=car.name,
            battery_capacity=car.battery_capacity,
            consumpting=car.consumpting,
            type_charger=car.type_charger
            )
            for car in cars
    ]

    db.add_all(car_objects)
    await db.flush()
    return car_objects

async def get_all_cars(db: AsyncSession) -> list[CarGet]:
    stmt = select(Car)

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_car_by_name(db: AsyncSession, name: str) -> CarGet | None:
    stmt = select(Car).where(Car.name == name)

    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_car(db: AsyncSession, id: int) -> CarGet | None:
    stmt = select(Car).where(Car.id == id)

    result = await db.execute(stmt)
    return result.scalar_one_or_none()

