from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from database.models import Base

#TODO Base.metadata.create_all() я не помню где и как в этой структуре делать

app = FastAPI()


