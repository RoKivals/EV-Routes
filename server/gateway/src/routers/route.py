from fastapi import APIRouter, Request
import httpx
from config import SERVICES

router = APIRouter()

@router.post("/distance_between_points")
async def add_station(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['route']}/distance_between_points", content=body, headers=request.headers)
        return response.json()