from fastapi import APIRouter, Request
import httpx
from config import SERVICES

router = APIRouter()

@router.get("/get_extra_stations")
async def add_car(request: Request):
    query_params = str(request.query_params)
    async with httpx.AsyncClient() as client:
        request_url = f"{SERVICES['route']}/get_path"
        if query_params:
            request_url += f"?{query_params}"

        response = await client.get(request_url)
        response.raise_for_status()
        return response.json()
