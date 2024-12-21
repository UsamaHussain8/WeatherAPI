import os
import environ
import json
import requests
from datetime import datetime, timedelta, timezone

env = environ.Env()
environ.Env.read_env()
API_KEY = env('API_KEY')

def get_city_geopoints(city):
    geo_json_response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}")
    city_data = json.loads(geo_json_response.text)

    return city_data

def get_city_name(city_lat, city_long):
    geo_json_response = requests.get(f"http://api.openweathermap.org/geo/1.0/reverse?lat={city_lat}&lon={city_long}&limit=1&appid={API_KEY}")
    city_data = json.loads(geo_json_response.text)

    return city_data[0]["name"]

def get_datetime(weather_data, time):    
    utc_time = datetime.fromtimestamp(weather_data['current'][time], tz=timezone.utc)    
    local_time = utc_time + timedelta(hours=5)
    if time == "sunrise" or time == "sunset":
        local_time = local_time.time()

    return local_time