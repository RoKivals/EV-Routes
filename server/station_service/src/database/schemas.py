from pydantic import BaseModel

class StationCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    connection_type: str
    power_kw: int | None

class StationGet(BaseModel): 
    id: int
    name: str
    latitude: float
    longitude: float
    connection_type: str
    power_kw: int | None = None
