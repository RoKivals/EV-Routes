from fastapi import APIRouter
from pydantic import BaseModel
import psycopg2

router = APIRouter()

conn = psycopg2.connect(dbname="evroutesuserinfo", user="roki", password="roki", host="localhost")
cursor = conn.cursor()

class UserData(BaseModel):
    email: str
    car_model: str
    battery_capacity: float
    connector_type: str

@router.post("/")
def save_user(data: UserData):
    cursor.execute(
        """
        INSERT INTO users (email, car_model, battery_capacity, connector_type)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (email) DO UPDATE SET
            car_model = EXCLUDED.car_model,
            battery_capacity = EXCLUDED.battery_capacity,
            connector_type = EXCLUDED.conector_type
        """,
        (data.email, data.car_model, data.battery_capacity, data.connector_type)
    )
    conn.commit()
    return {"status": "saved"}

@router.get("/{email}")
def get_user(email: str):
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    return row