from fastapi import APIRouter
from pydantic import BaseModel
import psycopg2

router = APIRouter()

conn = psycopg2.connect(dbname="evroutesstations", user="roki", password="roki", host="localhost")
cursor = conn.cursor()

class Station(BaseModel):
    name: str
    latitude: float
    longitude: float
    connector_type: str
    power_kW: int
    working_hours: str

@router.post("/")
def add_station(station: Station):
    cursor.execute(
        """
        INSERT INTO stations (name, latitude, longitude, connector_type, power_kW, working_hours)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (station.name, station.latitude, station.longitude, station.connector_type, station.power_kW, station.working_hours)
    )
    conn.commit()
    return {"status": "ok"}

@router.get("/")
def get_stations():
    cursor.execute("SELECT * FROM stations")
    rows = cursor.fetchall()
    return rows