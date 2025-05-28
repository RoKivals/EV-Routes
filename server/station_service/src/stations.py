import requests
from database.schemas import StationCreate
import os

API_BASE_URL = "https://api.openchargemap.io/v3"
API_KEY = "0693cf5e-35eb-460b-acb3-585ca9dd2547" #os.getenv("API_KEY")

URL_PARAMS = {
        'output': 'json',
        'key': API_KEY
    }

def get_ref_data_base_params():
    '''
    Возвращает описание возможных значений полей по нужным направлениям:
    1) Типы зарядок
    2) Страны
    '''
    new_url = f"{API_BASE_URL}/referencedata?{'&'.join(f'{key}={value}' for key, value in URL_PARAMS.items())}"
    response = requests.get(new_url)
    response.raise_for_status()
    data = response.json()
    
    conn_types = data['ConnectionTypes']
    countries = data['Countries']
    return conn_types, countries

def get_good_charg_ids():
    result_id = []
    GOOD_CHARG = ['CHAdeMO', 'CCS (Type 1)', 'CCS (Type 2)']
    connectors, _ = get_ref_data_base_params()

    for conn in connectors:
        if conn['Title'] in GOOD_CHARG:
            result_id.append(conn['ID'])
    return result_id

def get_all_info_by_country(country_id: int, connector_ids: list[int] = [2, 32, 33]):
    result = []
    new_url = f"""{API_BASE_URL}/poi?{'&'.join(f'{key}={value}' for key, value in URL_PARAMS.items())}&countryid={country_id}&connectiontypeid={', '.join(str(charge_id) for charge_id in connector_ids)}"""
    
    response = requests.get(new_url)
    response.raise_for_status()
    data = response.json()
    for station in data:
        result.append(get_use_info_from_json(station=station))
    return result

def get_use_info_from_json(station: dict) -> StationCreate:
    address_info = station['AddressInfo']
    name = address_info['Title']
    latitude = address_info['Latitude']
    longtitude = address_info['Longitude']
    connections_info = station['Connections']
    
    for connection in connections_info:
        connection_type = connection['ConnectionType']['Title']
        power_kw = connection['PowerKW']
        if connection['PowerKW'] is not None:
            power_kw = int(connection['PowerKW'])
        

    return StationCreate(name=name,
                        latitude=latitude,
                        longtitude=longtitude, 
                        connection_type=connection_type,
                        power_kw=power_kw
                        )

def all_stations_info():
    stations = []
    for country_id in range(251):
        country_stations = get_all_info_by_country(country_id=country_id)
        stations.extend(country_stations)
    return stations

if __name__ == '__main__':
    stations = all_stations_info()

    print(stations)