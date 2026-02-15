from pydantic import BaseModel

class StationGet(BaseModel): 
    id: int
    name: str
    latitude: float
    longitude: float
    connection_type: str
    power_kw: int | None = None

class MapPoint(BaseModel):
    latitude: float
    longitude: float

    def __iter__(self):
        yield self.latitude
        yield self.longitude