from database.schemas import Carpy
from database.models import Car

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def push_cars_data(db: AsyncSession, car: Carpy) -> Car:
    new_car = Car(id=car.id, )
    db.add(new_car)
    await db.flush()
    return new_car