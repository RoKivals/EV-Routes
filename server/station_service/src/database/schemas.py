from pydantic import BaseModel

class StationCreate(BaseModel):
    name: str
    latitude: float
    longtitude: float
    connection_type: str
    power_kw: int

class StationGet(BaseModel):
    id: int
    name: str
    latitude: float
    longtitude: float
    connection_type: str
    power_kw: int