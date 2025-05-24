from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from database.models import Base
from EV_cars import parse_ev_cars

#TODO Base.metadata.create_all() я не помню где и как в этой структуре делать

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_models()