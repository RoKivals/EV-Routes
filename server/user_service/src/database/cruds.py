from database.schemas import UserCreate, UserGet, UserInDB
from database.models import User
from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
async def add_user(db: AsyncSession, user: UserCreate) -> UserGet:
    hashed_password = pwd_context.hash(user.password.get_secret_value())
    new_user = User(login=user.login,
                    password_hash=hashed_password)
    try:
        db.add(new_user)
        await db.flush()
        return UserGet(id=new_user.id,
                    login=new_user.login,
                    car_id=new_user.car_id)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=f"Логин уже занят: {str(ie)}")

async def get_db_user(db: AsyncSession, login: str) -> UserInDB | None:
    stmt = select(User).where(User.login == login)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user(db: AsyncSession, login: str) -> UserGet | None:
    stmt = select(User).where(User.login == login)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

async def update_user_car(db: AsyncSession, login: int, new_car: int | None) -> UserGet:
    query = select(User).where(User.login == login)
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