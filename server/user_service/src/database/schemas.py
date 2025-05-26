from pydantic import BaseModel, SecretStr

class UserCreate(BaseModel):
    login: str
    password: SecretStr  
    car_id: int | None

class UserInDB(BaseModel):
    login: str
    password_hash: str
    car_id: int | None

class UserGet(BaseModel):
    id: int
    login: str
    car_id: str | None