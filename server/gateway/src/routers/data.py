from fastapi import APIRouter, Request
import httpx
from config import SERVICES

router = APIRouter()

@router.post("/add_car")
async def add_car(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['data']}/car", content=body, headers=request.headers)
        return response.json()
    
@router.post("/add_cars")
async def add_cars(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['data']}/cars", content=body, headers=request.headers)
        return response.json()

@router.get("/get_car_by_name")
async def get_car_by_name(request: Request):
    query_params = str(request.query_params)
    async with httpx.AsyncClient() as client:
        request_url = f"{SERVICES['data']}/car"
        if query_params:
            request_url += f"?{query_params}"

        response = await client.get(request_url)
        response.raise_for_status()
        return response.json()
    

@router.get("/get_car/{car_id}")
async def get_user_by_login(car_id: int, request: Request):
    query_params = str(request.query_params)
    async with httpx.AsyncClient() as client:
        request_url = f"{SERVICES['data']}/car/{car_id}"
        if query_params:
            request_url += f"?{query_params}"

        response = await client.get(request_url)
        response.raise_for_status()
        return response.json()
    

@router.get("/get_cars")
async def update_user_car(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['data']}/cars", content=body, headers=request.headers)
        return response.json()
