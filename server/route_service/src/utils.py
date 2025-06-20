from geopy.distance import geodesic
from dataclasses import dataclass
import requests
from database.schemas import StationGet

import os

import geopandas as gpd
from shapely.geometry import LineString, Point, MultiPoint
from shapely.ops import nearest_points

from heapq import heappush, heappop
from dataclasses import dataclass
from typing import List, Tuple, Set

@dataclass
class MapPoint:
    latitude: float
    longitude: float

    def __iter__(self):
        yield self.latitude
        yield self.longitude

@dataclass
class State:
    position: Tuple[float, float] 
    battery_level: float 
    cost: float 
    path: List[Tuple[float, float]]

def get_geo_distance(point_a: MapPoint, point_b: MapPoint):
    return geodesic(point_a, point_b).kilometers

def get_road_distance(point_a: MapPoint, point_b: MapPoint) -> float:
    url = f"http://router.project-osrm.org/route/v1/driving/{point_a.longitude},{point_a.latitude};{point_b.longitude},{point_b.latitude}"
    response = requests.get(url).json()
    print(response)
    distance_km = response["routes"][0]["distance"] / 1000
    return distance_km

def get_coordinates(api_key: str, location_name: str) -> tuple[float, float] | None:
    base_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": os.getenv(api_key),
        "geocode": location_name,
        "format": "json",
        "results": 1
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data["response"]["GeoObjectCollection"]["featureMember"]:
            geo_object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            pos = geo_object["Point"]["pos"].split()
            longitude, latitude = float(pos[0]), float(pos[1])
            return latitude, longitude
            
    except Exception as e:
        print(f"Ошибка при обработке ответа: {e}")
    
    return None

def get_close_stations_to_route(point_a: MapPoint, point_b: MapPoint, stations: list[StationGet], radius_search: int = 90_000) -> list[StationGet]:
    if not stations:
        return []

    # Создаём прямой путь от А до Б
    route_points = [(point_a.longitude, point_a.latitude),
                        (point_b.longitude, point_b.latitude)]
    route_line = LineString(route_points)

    route_geo_frame = gpd.GeoDataFrame(geometry=[route_line], crs="EPSG:4326")
    route_geo_frame = route_geo_frame.to_crs("EPSG:3857")
    buffer_zone = route_geo_frame.geometry.iloc[0].buffer(radius_search)

    poi_geo_frame = gpd.GeoDataFrame(
        data=[station.model_dump() for station in stations],
        geometry=gpd.points_from_xy([station.longtitude for station in stations],
                                    [station.latitude for station in stations]),
        crs="EPSG:4326"
    )
    poi_geo_frame = poi_geo_frame.to_crs(route_geo_frame.crs)

    within_mask = poi_geo_frame.geometry.within(buffer_zone)
    poi_in_buffer = poi_geo_frame[within_mask]
    
    if len(poi_in_buffer) > 0:
        selected_indices = poi_in_buffer.index.tolist()
        print(selected_indices)
        return [stations[i] for i in selected_indices]
    else:
        return []


def modified_dijkstra(start, end, initial_battery, min_battery_percent, 
                     consumption_per_km, charging_stations):
    
    # Приоритетная очередь: (стоимость, состояние)
    pq = [(0, State(start, initial_battery, 0, []))]
    
    # Множество посещенных состояний (позиция, заряд батареи округленный до 1 знака)
    visited = set()
    
    while pq:
        current_cost, current_state = heappop(pq)
        
        # Создаем ключ состояния для избежания повторных посещений
        if isinstance(current_state.position, tuple):
            pos_key = current_state.position
        else:
            pos_key = tuple(current_state.position)
            
        state_key = (pos_key, round(current_state.battery_level, 1))
        
        if state_key in visited:
            continue
        visited.add(state_key)
        
        # Проверяем, можем ли добраться до цели напрямую
        current_pos = current_state.position
        if not isinstance(current_pos, tuple):
            current_pos = tuple(current_pos)
            
        dist_to_end = get_road_distance(current_pos, end)
        battery_needed_to_end = dist_to_end * consumption_per_km
        
        # Если можем добраться до цели с достаточным запасом
        if current_state.battery_level >= battery_needed_to_end + min_battery_percent:
            final_battery = current_state.battery_level - battery_needed_to_end
            return {
                'success': True,
                'total_distance': current_cost + dist_to_end,
                'path_coordinates': [start] + [tuple(sid.position) 
                                             for sid in current_state.path] + [end],
                'charging_stations': current_state.path,
                'final_battery': final_battery
            }
        
        # Ищем ближайшие заправочные станции
        nearby_stations = get_close_stations_to_route(point_a=start, point_b=end, stations=charging_stations)
        
        for station in nearby_stations:
            station_pos = (station['lat'], station['lon'])
            dist_to_station = get_road_distance(current_pos, station_pos)
            battery_needed_to_station = dist_to_station * consumption_per_km
            
            # Проверяем, можем ли добраться до станции с минимальным запасом
            if current_state.battery_level >= battery_needed_to_station + min_battery_percent:
                # Переход к станции (зарядка без дополнительной стоимости)
                new_battery = 100.0
                new_cost = current_cost + dist_to_station  # только расстояние
                new_path = current_state.path + [station['id']]
                
                new_state = State(
                    station['id'],
                    new_battery,
                    new_cost,
                    new_path
                )
                
                heappush(pq, (new_cost, new_state))
    
    # Маршрут не найден
    return {
        'success': False,
        'total_distance': float('inf'),
        'path_coordinates': [],
        'charging_stations': [],
        'final_battery': 0
    }