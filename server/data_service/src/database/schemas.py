from pydantic import BaseModel

class CarCreate(BaseModel):
    name: str
    battery_capacity: str
    consumpting: str
    type_charger: str