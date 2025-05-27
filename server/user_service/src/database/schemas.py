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
    car_id: int | None

class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str
    exp: datetime | None = None
    scopes: list[str] = []
