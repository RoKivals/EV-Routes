from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database.schemas import StationGet, MapPoint
from utils import get_road_distance


app = FastAPI(title="EV Route Car Service")
app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST"],
    allow_origins=["*"]
)

@app.post("/distance_between_points")
async def get_distance(start: MapPoint, end: MapPoint):
    distance = get_road_distance(start, end)
    return {"distance_km": distance}