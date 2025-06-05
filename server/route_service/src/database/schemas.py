from pydantic import BaseModel

class StationGet(BaseModel): 
    id: int
    name: str
    latitude: float
    longtitude: float
    connection_type: str
    power_kw: int | None = None