from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from database.init_db import init_models
from contextlib import asynccontextmanager
from database import cruds
from database.schemas import UserCreate, UserGet, UserLogin
from auth.auth import authenticate_user, create_access_token
from config import ServiceLogger

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting up")
        app.add_middleware(
            allow_methods=["GET", "POST", "PATCH"],
            allow_origins=["*"]
        )
        await init_models()
        yield
    finally:
        print("Shutting down...")

app = FastAPI(lifespan=lifespan, title="EV Route User Service")
logger = ServiceLogger()

@app.post("/register", response_model=UserGet, status_code=status.HTTP_201_CREATED)
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info("")
    return await cruds.add_user(db, user)

@app.post("/login", response_model=UserGet)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, user_data.login, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user", response_model=UserGet)
async def get_user(login: str, db: AsyncSession = Depends(get_db)):
    return await cruds.get_user(db, login)

@app.patch("/user/car", response_model=UserGet, status_code=status.HTTP_202_ACCEPTED)
async def update_car(login: str, new_car: int, db: AsyncSession = Depends(get_db)):
    return await cruds.update_user_car(db, login, new_car)