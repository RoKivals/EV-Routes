from fastapi import APIRouter, Request
import httpx
from config import SERVICES

router = APIRouter()

@router.post("/register")
async def add_user(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['auth']}/register", content=body, headers=request.headers)
        return response.json()

@router.post("/login")
async def login(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['auth']}/login", content=body, headers=request.headers)
        return response.json()

@router.get("/user_by_login")
async def get_user_by_login(request: Request):
    query_params = str(request.query_params)
    async with httpx.AsyncClient() as client:
        request_url = f"{SERVICES['auth']}/user"
        if query_params:
            request_url += f"?{query_params}"

        response = await client.get(request_url)
        response.raise_for_status()
        return response.json()
    
@router.get("/user_change_car")
async def update_user_car(request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['auth']}/user/car", content=body, headers=request.headers)
        return response.json()
