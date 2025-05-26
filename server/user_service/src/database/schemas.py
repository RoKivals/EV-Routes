from pydantic import BaseModel, SecretStr
from datetime import datetime

class UserLogin(BaseModel):
    login: str
    password: SecretStr

class UserCreate(BaseModel):
    login: str
    password: SecretStr  

class UserInDB(BaseModel):
    login: str
    password_hash: str

class UserGet(BaseModel):
    id: int
    login: str
    car_id: str | None

class TokenData(BaseModel):
    sub: str
    exp: datetime | None = None
    scopes: list[str] = []

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp()  # Для корректной сериализации в JSON
        }