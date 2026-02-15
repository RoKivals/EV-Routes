from datetime import timedelta
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from database.init_db import init_models
from contextlib import asynccontextmanager
from database import cruds
from database.schemas import TokenData, UserCreate, UserGet, UserLogin, AccessToken
from auth.auth import AuthService
from logger_config import logger
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting up")
        await init_models()
        yield
    finally:
        print("Shutting down...")

app = FastAPI(lifespan=lifespan, title="EV Route User Service")
app.add_middleware(
CORSMiddleware,
                allow_methods=["GET", "POST", "PATCH"],
                allow_origins=["*"]
)

secret_key = os.getenv("SECRET_KEY")
auth_service = AuthService(secret_key=secret_key)

@app.post("/register", response_model=UserGet, status_code=status.HTTP_201_CREATED)
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info("Начали регистрацию")
    return await cruds.add_user(db, user)

@app.post("/login", response_model=AccessToken)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await auth_service.authenticate_user(db, user_data.login, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    access_token = auth_service.create_access_token(
        data=TokenData(sub=user.login),
        expires_delta=timedelta(minutes=30)
        )
    return AccessToken(access_token=access_token)

@app.get("/user", response_model=UserGet)
async def get_user(login: str, db: AsyncSession = Depends(get_db)):
    return await cruds.get_user(db, login)

@app.patch("/user/car", response_model=UserGet, status_code=status.HTTP_202_ACCEPTED)
async def update_car(login: str, new_car: int, db: AsyncSession = Depends(get_db)):
    return await cruds.update_user_car(db, login, new_car)