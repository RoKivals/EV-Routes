from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RouteRequest(BaseModel):
    start: str
    end: str
    battery_level: int

@router.post("/")
def calculate_route(data: RouteRequest):
    return {
        "start": data.start,
        "end": data.end,
        "estimated_time": "2h 30m",
        "stations_on_route": []
    }