from database.schemas import UserCreate, UserGet, UserInDB
from database.models import User
from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
async def add_user(db: AsyncSession, user: UserCreate) -> UserGet:
    hashed_password = pwd_context.hash(user.password.get_secret_value())

    new_user = UserInDB(login=user.login,
                        password_hash=hashed_password,
                        car_id=user.car_id
                        )
    
    db.add(new_user)
    db.flush()
    return UserGet(id=new_user.id,
                   login=new_user.login,
                   car_id=new_user.car_id)


async def get_db_user(db: AsyncSession, login: str) -> UserInDB | None:
    stmt = select(User).where(User.login == login)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user(db: AsyncSession, login: str) -> UserGet | None:
    stmt = select(User).where(User.login == login)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_user_car(db: AsyncSession, login: int, new_car: int | None) -> UserGet:
    query = select(UserInDB).where(UserInDB.login == login)
    result = await db.execute(statement=query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.car_id = new_car
    await db.flush()

    return UserGet(
        id=user.id,
        login=user.login,
        car_id=user.car_id)