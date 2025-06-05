from geopy.distance import geodesic
from dataclasses import dataclass
import requests
from database.schemas import StationGet

from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import String, Float, Integer

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import geopandas as gpd
from shapely.geometry import LineString, Point, MultiPoint
from shapely.ops import nearest_points


@dataclass
class MapPoint:
    latitude: float
    longitude: float

    def __iter__(self):
        yield self.latitude
        yield self.longitude

def get_geo_distance(point_a: MapPoint, point_b: MapPoint):
    return geodesic(point_a, point_b).kilometers

# OSRM maps API
def get_road_distance(point_a: MapPoint, point_b: MapPoint) -> float:
    url = f"http://router.project-osrm.org/route/v1/driving/{point_a.longitude},{point_a.latitude};{point_b.longitude},{point_b.latitude}"
    response = requests.get(url).json()
    print(response)
    distance_km = response["routes"][0]["distance"] / 1000
    return distance_km

def get_close_stations_to_route(point_a: MapPoint, point_b: MapPoint, stations: list[StationGet], radius_search: int = 90_000):
    route_points = [point_a, point_b]

    route_line = LineString(route_points)
    route_geo_frame = gpd.GeoDataFrame(geometry=[route_line], crs="EPSG:4326")
    route_geo_frame = route_geo_frame.to_crs("EPSG:3857")

    buffer_zone = route_geo_frame.buffer(radius_search)

    poi_geo_frame = gpd.GeoDataFrame(
        data=[station.model_dump() for station in stations],
        geometry=gpd.points_from_xy([station.longtitude for station in stations],
                                    [station.latitude for station in stations]),
        crs="EPSG:4326"
    )
    poi_geo_frame = poi_geo_frame.to_crs(route_geo_frame.crs)
    
    poi_in_buffer = poi_geo_frame[poi_geo_frame.within(buffer_zone)]
    print(f"Найдено {len(poi_in_buffer)} POI в радиусе от маршрута")


def main():
    kiev = MapPoint(50.450441, 30.523550)
    lvov = MapPoint(49.839323, 24.029898)

    class Base(DeclarativeBase):
        pass

    # Модель Station
    class Station(Base):
        __tablename__ = "stations"

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)  # Указал длину String
        latitude: Mapped[float] = mapped_column(Float, index=True, nullable=False)
        longtitude: Mapped[float] = mapped_column(Float, index=True, nullable=False)  # Исправлено опечатку (было longtitude)
        connection_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
        power_kw: Mapped[int] = mapped_column(Integer, nullable=True)  # Исправлено __name_pos на Integer



    # Подключение к PostgreSQL (используя psycopg2)
    DATABASE_URL = "postgresql+psycopg2://fastapi:secret@postgres:5432/fastapi_dev"
    engine = create_engine(DATABASE_URL)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        query = select(Station)  # Или select(Station.name, Station.latitude)
        result = session.execute(query).scalars().all()  # Получаем все записи
        stations: list[StationGet] = [
            StationGet(
                id=station.id,
                name=station.name,
                latitude=station.latitude,
                longtitude=station.longtitude,
                connection_type=station.connection_type,
                power_kw=station.power_kw
            )
            for station in result
        ]
        get_close_stations_to_route(kiev, lvov, stations)


    finally:
        # Закрываем сессию и соединение
        session.close()
        engine.dispose()

