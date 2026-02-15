from fastapi import APIRouter, Request
import httpx
from config import SERVICES

router = APIRouter()

@router.post("/add_station")
async def add_station(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['station']}/station", content=body, headers=request.headers)
        return response.json()

@router.post("/add_stations")
async def login(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['station']}/stations", content=body, headers=request.headers)
        return response.json()

@router.get(path="/all_stations")
async def get_user_by_login(request: Request):
    query_params = str(request.query_params)
    async with httpx.AsyncClient() as client:
        request_url = f"{SERVICES['station']}/stations"
        if query_params:
            request_url += f"?{query_params}"

        response = await client.get(request_url)
        response.raise_for_status()
        return response.json()